from calc.base import *
from calc.base import find_initial_guesses

def bolzano_theorem(func, variables):
    lambda_func = parse_expression_to_lambda(func, variables)
    intervals = find_initial_guesses(lambda_func)
    return intervals

def bisection_method(func, variables, tolerance=1e-5, max_iterations=100, max_expansions=100):
    # Converte a função para um lambda
    lambda_func = parse_expression_to_lambda(func, variables)
    
    # Encontra todos os intervalos com mudança de sinal usando a função find_initial_guesses
    intervals = find_initial_guesses(lambda_func)
    
    # Lista para armazenar as raízes encontradas
    roots = []

    # Aplica o método da bisseção em cada intervalo encontrado
    for a, b in intervals:
        iterations = 0
        while (b - a) / 2 > tolerance and iterations < max_iterations:
            # Calcula o ponto médio
            midpoint = (a + b) / 2
            f_mid = lambda_func(midpoint)
            
            # Checa se encontramos a raiz
            if abs(f_mid) < tolerance:
                if all(abs(midpoint - r) > tolerance for r in roots):  # Evitar duplicatas
                    roots.append(midpoint)
                break
            
            # Aplica o teorema de Bolzano para decidir o próximo intervalo
            if lambda_func(a) * f_mid < 0:
                b = midpoint  # A raiz está no intervalo [a, midpoint]
            else:
                a = midpoint  # A raiz está no intervalo [midpoint, b]
            
            iterations += 1

        # Adiciona o ponto médio como uma raiz aproximada, se não foi adicionada anteriormente
        else:
            midpoint = (a + b) / 2
            if all(abs(midpoint - r) > tolerance for r in roots):  # Evitar duplicatas
                roots.append(midpoint)

    return roots

def newton_raphson_method(func, variables, tolerance=1e-5, max_iterations=1000):
    # Converte a função para um lambda
    lambda_func = parse_expression_to_lambda(func, variables)

    # Encontra todos os intervalos com mudanças de sinal
    intervals = find_initial_guesses(lambda_func)

    # Deriva a função para obter a função derivada
    derivative_func, _ = derive_lambda_function(lambda_func)

    # Lista para armazenar as raízes encontradas
    roots = []

    for a, b in intervals:
        # Usa o ponto médio do intervalo como chute inicial
        x = (a + b) / 2

        for i in range(max_iterations):
            f_x = lambda_func(x)
            f_prime_x = derivative_func(x)

            # Evita divisão por zero na derivada
            if abs(f_prime_x) < tolerance:
                break

            # Calcula a próxima aproximação de x
            x_next = x - f_x / f_prime_x

            # Verifica a convergência
            if abs(x_next - x) < tolerance:
                # Adiciona a raiz se não for duplicada
                if all(abs(x_next - root) > tolerance for root in roots):
                    roots.append(x_next)
                break

            x = x_next  # Atualiza x para a próxima iteração

    if not roots:
        raise Exception("Não foi possível encontrar raízes no intervalo fornecido.")

    return roots

def secant_method(func, variables, tolerance=1e-5, max_iterations=100):
    lambda_func = parse_expression_to_lambda(func, variables)

    # Encontra todos os intervalos com mudanças de sinal
    intervals = find_initial_guesses(lambda_func)

    # Lista para armazenar as raízes encontradas
    roots = []

    roots = []

    for a, b in intervals:
        # Inicializa x0 e x1 como os extremos do intervalo
        x0, x1 = a, b

        for i in range(max_iterations):
            f_x0 = lambda_func(x0)
            f_x1 = lambda_func(x1)



            # Evita divisão por zero na diferença
            if abs(f_x1 - f_x0) < tolerance:
                break

            # Calcula a próxima aproximação de x usando o método da secante
            x_next = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)

            # Verifica a convergência
            if abs(x_next - x1) < tolerance:
                # Adiciona a raiz se não for duplicada
                if all(abs(x_next - root) > tolerance for root in roots):
                    roots.append(x_next)
                break

            # Atualiza os pontos x0 e x1 para a próxima iteração
            x0, x1 = x1, x_next

    if not roots:
        raise Exception("Não foi possível encontrar raízes no intervalo fornecido.")

    return roots
