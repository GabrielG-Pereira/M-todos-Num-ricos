from calc.eq_lineares import *
from calc.si_lineares import *
from calc.interpolacao import *
from calc.integracao import *
from calc.extrapolacao import *
from flask import Flask, render_template, jsonify, request, redirect, url_for


RESULTS_FILE = "results.json"

subgruposOptions = {
    "equacoes-lineares": ["Teorema de Bolzano", "Método da Bissecção", "Método de Newton-Raphson", "Método da Secante"],
    "sistemas-lineares": ["Eliminação de Gauss", "Método de Gauss-Jacobi", "Metodos iterativos", "Método de Gauss-Seidel"],
    "interpolacao": ["Interpolação Lagrange", "Interpolação Newton-Gregory", "Interpolação Inversa"],
    "extrapolacao": ["Método dos mínimos quadrados"],
    "integracao": ["Método do Trapezio Composto"]
}

app = Flask(__name__)

functions_map = {
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/funcao')
def funcao():
    texto = request.args.get('texto', '')
    escrever_arquivo(texto)
    return render_template('funcao.html')

@app.route('/obter_texto', methods=['GET'])
def obter_texto():
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
            resultado_formatado = str(", ".join(f"{var}: {dynamic_round(float(valor))}" for var, valor in resultado.items()))
            return jsonify({"result" : dynamic_round_in_string(resultado_formatado)})
        elif subgrupo == "método-de-gauss-jacobi":
            resultado = gauss_jacobi_from_expressions(expressao, variaveis)
            resultado_formatado = ", ".join(f"{var}: {dynamic_round(float(valor))}" for var, valor in resultado.items())
            return jsonify({"result" : dynamic_round_in_string(resultado_formatado)})
        elif subgrupo == "metodos-iterativos":
            resultado = newton_method_system(expressao, variaveis)
            resultado_formatado = ", ".join(f"{var}: {dynamic_round(float(valor))}" for var, valor in resultado.items())
            return jsonify({"result" : dynamic_round_in_string(resultado_formatado)})
        elif subgrupo == "método-de-gauss-seidel":
            resultado = gauss_seidel_from_expressions(expressao, variaveis)
            resultado_formatado = ", ".join(f"{var}: {dynamic_round(float(valor))}" for var, valor in resultado.items())
            return jsonify({"result" : dynamic_round_in_string(resultado_formatado)})
        

        elif subgrupo == "interpolação-lagrange":
            func, _ = lagrange_interpolating_polynomial(string_to_tuple_list(pontos))
            return jsonify({"result" : dynamic_round_in_string(str(func))})
        elif subgrupo == "interpolação-newton-gregory":
            text = newton_gregory_forward(x, y, valor)
            return jsonify({"result" : dynamic_round_in_string(text)})
        elif subgrupo == "interpolação-inversa":
            linear_func, a, b = least_squares_linear(x, y)
            text = f"Função: y = {a:f} + {b:f}x"
            return jsonify({"result" : dynamic_round_in_string(text)})


        elif subgrupo == "método-dos-mínimos-quadrados":
            print(pontos)
            result = least_squares_quadratic_extrapolation(string_to_tuple_list(pontos))
            resultado_formatado = ", ".join(f"{var}: {dynamic_round(float(valor))}" for var, valor in result["coefficients"].items())
            text = f"Função: {result["formula"]}\nCoeficientes: {resultado_formatado}"
            return jsonify({"result" : dynamic_round_in_string(text)})
        
        elif subgrupo == "método-do-trapezio-composto":
            text = str(compound_trace_method(expressao[0], x[0], y[0], int(valor)))
            return jsonify({"result" : dynamic_round_in_string(text)})
        return jsonify({"result" :"Selecione um método!"})

    except Exception as e:
        return jsonify({"result": str(e)})
    
def dynamic_round(number, repeat_threshold=5):
    print(type(number))
    num_str = f"{number:.6f}".rstrip('0')  # Converter para string e remover zeros à direita
    decimal_part = num_str.split('.')[1] if '.' in num_str else ''
    repeat_count = 1
    for i in range(1, len(decimal_part)):
        if decimal_part[i] == decimal_part[i - 1]:
            repeat_count += 1
            if repeat_count >= repeat_threshold:
                return round(number, i - repeat_count + 1)
        else:
            repeat_count = 1

    return number

def dynamic_round_in_string(input_string, repeat_threshold=5, decimal_places=None):
    def dynamic_round_from_string(number_str, repeat_threshold):
        # Trabalha diretamente com a string para evitar imprecisões de float
        if '.' not in number_str:
            return number_str  # Retorna o número original se não tiver parte decimal
        
        # Separa a parte inteira e a decimal
        integer_part, decimal_part = number_str.split('.')
        repeat_count = 1

        for i in range(1, len(decimal_part)):
            if decimal_part[i] == decimal_part[i - 1]:
                repeat_count += 1
                if repeat_count >= repeat_threshold:
                    # Arredonda até a posição onde a repetição começa
                    rounded_number = f"{integer_part}.{decimal_part[:i - repeat_count + 1]}"
                    return str(float(rounded_number))  # Remove zeros desnecessários ao final
            else:
                repeat_count = 1

        return number_str  # Retorna o número original se nenhuma repetição for encontrada

    # Regex para identificar números (incluindo negativos e decimais)
    number_pattern = re.compile(r"-?\d+(\.\d+)?")
    
    # Função para substituir números pelo número arredondado
    def replace_number(match):
        original_number_str = match.group()
        rounded_number_str = dynamic_round_from_string(original_number_str, repeat_threshold)
        return rounded_number_str

    # Substituir números na string
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

def escrever_arquivo(texto):
    """Escreve o texto em um arquivo."""
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as file:
            file.write(texto)
        print(f"Texto escrito com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao escrever no arquivo: {e}")

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

if __name__ == '__main__':
    app.run(debug=True, port=5003)