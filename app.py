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
            return jsonify({"result" : bolzano_theorem(expressao[0])})
        elif subgrupo == "método-da-bissecção":
            return jsonify({"result" : bisection_method(expressao[0])})
        elif subgrupo == "método-de-newton-raphson":
            return jsonify({"result" : newton_raphson_method(expressao[0])})
        elif subgrupo == "método-da-secante":
            return jsonify({"result" : secant_method(expressao[0])})
        

        elif subgrupo == "eliminação-de-gauss":
            resultado = gauss_elimination_from_expressions(expressao, variaveis)
            resultado_formatado = ", ".join(f"{var}: {float(valor)}" for var, valor in resultado.items())
            return jsonify({"result" : resultado_formatado})
        elif subgrupo == "método-de-gauss-jacobi":
            resultado = gauss_jacobi_from_expressions(expressao, variaveis)
            resultado_formatado = ", ".join(f"{var}: {float(valor)}" for var, valor in resultado.items())
            return jsonify({"result" : resultado_formatado})
        elif subgrupo == "metodos-iterativos":
            resultado = newton_method_system(expressao, variaveis)
            resultado_formatado = ", ".join(f"{var}: {float(valor)}" for var, valor in resultado.items())
            return jsonify({"result" : resultado_formatado})
        elif subgrupo == "método-de-gauss-seidel":
            resultado = gauss_seidel_from_expressions(expressao, variaveis)
            resultado_formatado = ", ".join(f"{var}: {float(valor)}" for var, valor in resultado.items())
            return jsonify({"result" : resultado_formatado})
        

        elif subgrupo == "interpolação-lagrange":
            func, _ = lagrange_interpolating_polynomial(string_to_tuple_list(pontos))
            return jsonify({"result" : str(func)})
        elif subgrupo == "interpolação-newton-gregory":
            return jsonify({"result" : newton_gregory_forward(x, y, valor)})
        elif subgrupo == "interpolação-inversa":
            linear_func, a, b = least_squares_linear(x, y)
            print(f"Equação da linha de ajuste: y = {a:.2f} + {b:.2f}x")
            return jsonify({"result" : f"y = {a:f} + {b:f}x"})


        elif subgrupo == "método-dos-mínimos-quadrados":
            return jsonify({"result" : least_squares_linear_extrapolation(x, y, valor)})
        
        elif subgrupo == "método-do-trapezio-composto":
            return jsonify({"result" : str(compound_trace_method(expressao[0], x[0], y[0], int(valor)))})

    except Exception as e:
        return jsonify({"result": str(e)})
    

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