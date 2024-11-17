import os
import sys
import threading
import webview
from calc.eq_lineares import *
from calc.si_lineares import *
from calc.interpolacao import *
from calc.integracao import *
from calc.extrapolacao import *
from flask import Flask, render_template, jsonify, request, redirect, url_for


if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

app = Flask(__name__, template_folder=os.path.join(base_path, 'templates'), static_folder=os.path.join(base_path, 'static'))

RESULTS_FILE = "results.json"

subgruposOptions = {
    "equacoes-lineares": ["Teorema de Bolzano", "Método da Bissecção", "Método de Newton-Raphson", "Método da Secante"],
    "sistemas-lineares": ["Eliminação de Gauss", "Método de Gauss-Jacobi", "Metodos iterativos", "Método de Gauss-Seidel"],
    "interpolacao": ["Interpolação Lagrange", "Interpolação Newton-Gregory", "Interpolação Inversa"],
    "extrapolacao": ["Método dos mínimos quadrados"],
    "integracao": ["Método do Trapezio Composto"]
}


functions_map = {
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/funcao')
def funcao():
    def escrever_arquivo(texto):
        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as file:
                file.write(texto)
        except Exception as e:
            print(f"Erro ao escrever no arquivo: {e}")
    texto = request.args.get('texto', '')
    escrever_arquivo(texto)
    return render_template('funcao.html')

@app.route('/obter_texto', methods=['GET'])
def obter_texto():
    def ler_arquivo():
        """Lê o conteúdo de um arquivo e retorna como string."""
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                conteudo = file.read()
            return conteudo
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return None

    def identificar_subgrupo(texto):
        """Identifica a chave em que o texto se encontra dentro de subgruposOptions."""
        for chave, opcoes in subgruposOptions.items():
            if texto in opcoes:
                return chave
        return None
    texto = ler_arquivo()
    return jsonify({
        "item": texto,
        "grup" : identificar_subgrupo(texto)
        })  # Retorna o texto em formato JSON

@app.route('/processar_dados', methods=['POST'])
def processar_dados():
    try:
        # Obtém os dados JSON do corpo da requisição
        dados = request.get_json()

        # Extrai os valores do dicionário 'dados'
        subgrupo = dados.get('subgrupo')
        expressao = dados.get('expressao')
        variaveis = extrair_variaveis(expressao[0])
        pontos = dados.get('pontos')
        try:
            x = [float(num.strip()) if '.' in num else int(num.strip()) for num in  dados.get('x').split(",")]
            y = [float(num.strip()) if '.' in num else int(num.strip()) for num in  dados.get('y').split(",")]
            valor = float(dados.get('valor'))
        except:
            pass   

        if subgrupo == "teorema-de-bolzano":
            text = str(bolzano_theorem(expressao[0], variaveis))
            return jsonify({"result" : dynamic_round_in_string(text)})
        elif subgrupo == "método-da-bissecção":
            text = str(bisection_method(expressao[0], variaveis))
            return jsonify({"result" : dynamic_round_in_string(text)})
        elif subgrupo == "método-de-newton-raphson":
            text = str(newton_raphson_method(expressao[0], variaveis))
            return jsonify({"result" : dynamic_round_in_string(text)})
        elif subgrupo == "método-da-secante":
            text = str(secant_method(expressao[0], variaveis))
            return jsonify({"result" : dynamic_round_in_string(text)})
        

        elif subgrupo == "eliminação-de-gauss":
            resultado = gauss_elimination_from_expressions(expressao, variaveis)
            resultado_formatado = str(", ".join(f"{var}: {float(valor)}" for var, valor in resultado.items()))
            return jsonify({"result" : dynamic_round_in_string(resultado_formatado)})
        elif subgrupo == "método-de-gauss-jacobi":
            resultado = gauss_jacobi_from_expressions(expressao, variaveis)
            resultado_formatado = ", ".join(f"{var}: {float(valor)}" for var, valor in resultado.items())
            return jsonify({"result" : dynamic_round_in_string(resultado_formatado)})
        elif subgrupo == "metodos-iterativos":
            resultado = newton_method_system(expressao, variaveis)
            resultado_formatado = ", ".join(f"{var}: {float(valor)}" for var, valor in resultado.items())
            return jsonify({"result" : dynamic_round_in_string(resultado_formatado)})
        elif subgrupo == "método-de-gauss-seidel":
            resultado = gauss_seidel_from_expressions(expressao, variaveis)
            resultado_formatado = ", ".join(f"{var}: {float(valor)}" for var, valor in resultado.items())
            return jsonify({"result" : dynamic_round_in_string(resultado_formatado)})
        

        elif subgrupo == "interpolação-lagrange":
            func, _ = lagrange_interpolating_polynomial(string_to_tuple_list(pontos))
            return jsonify({"result" : dynamic_round_in_string(str(func))})
        elif subgrupo == "interpolação-newton-gregory":
            text = newton_gregory_forward(x, y, valor)
            return jsonify({"result" : dynamic_round_in_string(str(text))})
        elif subgrupo == "interpolação-inversa":
            linear_func, a, b = least_squares_linear(x, y)
            text = f"Função: y = {a:f} + {b:f}x"
            return jsonify({"result" : dynamic_round_in_string(text)})


        elif subgrupo == "método-dos-mínimos-quadrados":
            print(pontos)
            result = least_squares_quadratic_extrapolation(string_to_tuple_list(pontos))
            print(result)
            resultado_formatado = ", ".join(f"{var}: {float(valor)}" for var, valor in result["coefficients"].items())
            text = f"Função: {result["formula"]}\nCoeficientes: {resultado_formatado}"
            return jsonify({"result" :dynamic_round_in_string(text)})
        
        elif subgrupo == "método-do-trapezio-composto":
            text = str(compound_trace_method(expressao[0], x[0], y[0], int(valor)))
            return jsonify({"result" : dynamic_round_in_string(text)})
        return jsonify({"result" :"Selecione um método!"})

    except Exception as e:
        return jsonify({"result": (e)})
    
def dynamic_round_in_string(input_string, repeat_threshold=5):
    def dynamic_round_from_string(number_str, repeat_threshold):
        if '.' not in number_str:
            return number_str  # Retorna o número original se não tiver parte decimal

        # Verifica e separa o sinal
        is_negative = number_str.startswith('-')
        if is_negative:
            number_str = number_str[1:]  # Remove o sinal para processamento

        integer_part, decimal_part = number_str.split('.')

        repeat_count = 1
        cutoff_index = None

        for i in range(1, len(decimal_part)):
            if decimal_part[i] == decimal_part[i - 1]:
                repeat_count += 1
                if repeat_count >= repeat_threshold:
                    cutoff_index = i - repeat_count + 2
                    break
            else:
                repeat_count = 1

        if cutoff_index:
            rounded_decimal = decimal_part[:cutoff_index]
            if cutoff_index < len(decimal_part) and int(decimal_part[cutoff_index]) >= 5:
                increment = 10 ** -cutoff_index
                rounded_number = float(f"{integer_part}.{rounded_decimal}") + increment
            else:
                rounded_number = float(f"{integer_part}.{rounded_decimal}")

            # Reaplica o sinal negativo, se necessário
            if is_negative:
                rounded_number = -rounded_number

            return str(rounded_number).rstrip('0').rstrip('.')

        # Reaplica o sinal negativo ao número original, se necessário
        return f"-{number_str}" if is_negative else number_str

    number_pattern = re.compile(r"-?\d+(\.\d+)?")

    def replace_number(match):
        original_number_str = match.group()
        rounded_number_str = dynamic_round_from_string(original_number_str, repeat_threshold)
        return rounded_number_str

    result_string = number_pattern.sub(replace_number, input_string)
    return result_string

caminho_arquivo = "txt.txt"

def string_to_tuple_list(input_string):
    """
    Converte uma string de pares como '(1, 2), (2, 3), (3, 5)'
    para uma lista de tuplas [(1, 2), (2, 3), (3, 5)].
    """
    # Remove espaços desnecessários e divide pelos parênteses
    pairs = input_string.strip().split("),")
    
    # Processa cada par removendo os parênteses e convertendo para inteiros
    result = [tuple(map(float, pair.strip("() ").split(","))) for pair in pairs]
    
    return result

def start_flask():
    app.run()

if __name__ == '__main__':
    api = webview.create_window(
        title='Translater', 
        url='http://127.0.0.1:5000',
        min_size=(650, 550) )

    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    webview.start()
    os._exit(1)