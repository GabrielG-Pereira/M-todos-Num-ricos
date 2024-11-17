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
    def identificar_subgrupo(texto):
        for chave, opcoes in subgruposOptions.items():
            if texto in opcoes:
                return chave
        return None
    
    item = request.args.get('texto', '')
    grup = identificar_subgrupo(item)
    return render_template('funcao.html', item = item, grup = grup)


@app.route('/processar_dados', methods=['POST'])
def processar_dados():
    try:

        methods = {
            "teorema-de-bolzano": lambda expr, vars: bolzano_theorem(expr[0], vars),
            "método-da-bissecção": lambda expr, vars: bisection_method(expr[0], vars),
            "método-de-newton-raphson": lambda expr, vars: newton_raphson_method(expr[0], vars),
            "método-da-secante": lambda expr, vars: secant_method(expr[0], vars),
            "eliminação-de-gauss": gauss_elimination_from_expressions,
            "método-de-gauss-jacobi": gauss_jacobi_from_expressions,
            "metodos-iterativos": newton_method_system,
            "método-de-gauss-seidel": gauss_seidel_from_expressions,
            "interpolação-lagrange": lagrange_interpolating_polynomial,
            "interpolação-newton-gregory": newton_gregory_forward,
            "interpolação-inversa": least_squares_linear,
            "método-dos-mínimos-quadrados": least_squares_quadratic_extrapolation,
            "método-do-trapezio-composto": compound_trace_method,
        }

        def string_to_tuple_list(input_string):
            pairs = input_string.strip().split("),")
            result = [tuple(map(float, pair.strip("() ").split(","))) for pair in pairs]
            return result

        # Obtém os dados JSON do corpo da requisição
        dados = request.get_json()

        # Extrai os valores do dicionário 'dados'
        subgrupo = dados.get('subgrupo')
        expressao = dados.get('expressao')
        variaveis = extrair_variaveis(expressao[0])
        pontos = dados.get('pontos')
        try:
            x_fonte = dados.get('x')
            y_fonte = dados.get('y')
            valor_fonte = dados.get('valor')
            x = [float(num.strip()) if '.' in num else int(num.strip()) for num in  x_fonte.split(",")]
            y = [float(num.strip()) if '.' in num else int(num.strip()) for num in  y_fonte.split(",")]
            valor = float(valor_fonte)
        except:
            pass   
                
        if subgrupo in methods:
            if subgrupo in ["interpolação-lagrange", "método-dos-mínimos-quadrados", "método-dos-mínimos-quadrados"]:
                if pontos == '':
                    raise Exception("Digite os pontos.")
                result = methods[subgrupo](string_to_tuple_list(pontos))
            elif subgrupo == "interpolação-newton-gregory":
                if x_fonte == '' or y_fonte == '' or valor_fonte == '':
                    raise Exception("Preencha todos os campos.")
                result = methods[subgrupo](x, y, valor)
            elif subgrupo == "interpolação-inversa":
                if x_fonte == '' or y_fonte == '':
                    raise Exception("Preencha todos os campos.")
                linear_func, a, b = methods[subgrupo](x, y)
                result = f"Função: y = {a:f} + {b:f}x"
            elif subgrupo == "método-do-trapezio-composto":
                if expressao[0] == '' or x_fonte == '' or y_fonte == '' or valor_fonte == '':
                    raise Exception("Preencha todos os campos.")
                result = methods[subgrupo](expressao, x, y, valor)
            else:
                if expressao[0] == '':
                    raise Exception("Digite uma função.")
                result = methods[subgrupo](expressao, variaveis)
            
            # Retornar o resultado
            return jsonify({"result": dynamic_round_in_string(str(result))})
        else:
            return jsonify({"result": (e)})

    except Exception as e:
        return jsonify({"result": str(e)})
    
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