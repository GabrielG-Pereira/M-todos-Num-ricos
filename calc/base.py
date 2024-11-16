import re
import numpy as np
import sympy as sp

def extrair_variaveis(expressao):
    # Remove "^" e substitui por "**" para compatibilidade, se necessário
    expressao = expressao.replace("^", "**")
    
    # Procura por letras que representam variáveis (isoladas ou com expoentes)
    variaveis = set(re.findall(r'\b([a-zA-Z])\b', expressao))
    
    return sorted(variaveis)

def parse_expression_to_lambda(expression, variables='x'):
    # Substitui "^" por "**" para compatibilidade com Python
    expression = expression.replace("^", "**")

    # Adiciona o prefixo np. para usar funções matemáticas do NumPy
    expression = re.sub(r'(\b(?:sin|cos|tan|log|exp|sqrt)\b)', r'np.\1', expression)

    # Constrói a expressão para resolver f(x, y) = 0 (ou mais variáveis)
    if '=' in expression:
        left, right = expression.split('=')
        expression = f"({left}) - ({right})"
    
    # Cria a função lambda a partir da expressão, com suporte a múltiplas variáveis
    lambda_func = eval(f"lambda {', '.join(variables)}: {expression}", {"np": np})
    return lambda_func

def derive_lambda_function(lambda_func):
    # Obtém o símbolo para a variável x
    x = sp.symbols('x')

    # Converte a função lambda para uma expressão simbólica
    expression = sp.sympify(lambda_func(x))

    # Calcula a derivada simbólica
    derivative_sympy = sp.diff(expression, x)

    # Converte a derivada para uma função lambda para uso numérico
    derivative_func = sp.lambdify(x, derivative_sympy, modules=['numpy'])

    return derivative_func, derivative_sympy

def find_initial_guesses(lambda_func, start=-100, end=100, num_intervals=1000, tolerance=1e-5):
    interval_length = (end - start) / num_intervals
    points = []
    visited_roots = []

    for i in range(num_intervals):
        a = start + i * interval_length
        b = a + interval_length

        try:
            # Verifica se há mudança de sinal
            if lambda_func(a) * lambda_func(b) < 0:
                midpoint = (a + b) / 2

                # Verifica se o ponto médio já está próximo de uma raiz encontrada
                if all(abs(midpoint - root) > tolerance for root in visited_roots):
                    points.append((a, b))
                    visited_roots.append(midpoint)
        except (ValueError, OverflowError):
            # Ignora erros na avaliação da função
            continue

    if not points:
        raise Exception("Não foi possível encontrar intervalos com mudança de sinal.")

    return points

def derive_jacobian_matrix(functions, variables):
    symbols = sp.symbols(variables)
    jacobian = []

    for func in functions:
        row = [
            sp.lambdify(symbols, sp.diff(func(*symbols), var), 'numpy')
            for var in symbols
        ]
        jacobian.append(row)

    return jacobian