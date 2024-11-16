from calc.base import *

def bolzano_theorem(func):
    lambda_func = parse_expression_to_lambda(func)
    return find_initial_guesses(lambda_func)

def bisection_method(func, tolerance=1e-5, max_iterations=100):

    lambda_func = parse_expression_to_lambda(func)
    a, b = find_initial_guesses(lambda_func)

    # Verifica se o teorema de Bolzano é válido no intervalo inicial
    if lambda_func(a) * lambda_func(b) >= 0:
        raise Exception("O teorema de Bolzano não é aplicável no intervalo fornecido.")
    
    # Variáveis para rastrear o número de iterações
    iterations = 0
    while (b - a) / 2 > tolerance and iterations < max_iterations:
        # Calcula o ponto médio
        midpoint = (a + b) / 2
        f_mid = lambda_func(midpoint)
        
        # Checa se encontramos a raiz
        if abs(f_mid) < tolerance:
            return midpoint
        
        # Aplica o teorema de Bolzano para decidir o próximo intervalo
        if lambda_func(a) * f_mid < 0:
            b = midpoint  # A raiz está no intervalo [a, midpoint]
        else:
            a = midpoint  # A raiz está no intervalo [midpoint, b]
        
        iterations += 1

    # Retorna o ponto médio como aproximação da raiz
    return (a + b) / 2

def newton_raphson_method(func, tolerance=1e-5, max_iterations=1000):
    lambda_func = parse_expression_to_lambda(func, variables=['x'])
    x, _ = find_initial_guesses(lambda_func)
    derivative_func, _ = derive_lambda_function(lambda_func)
    
    for i in range(max_iterations):
        f_x = lambda_func(x)
        f_prime_x = derivative_func(x)

        # Evita divisão por zero na derivada
        if abs(f_prime_x) < tolerance:
            raise Exception("Derivada próxima de zero. O método não convergiu.")

        # Calcula a próxima aproximação de x
        x_next = x - f_x / f_prime_x

        # Verifica a convergência
        if abs(x_next - x) < tolerance:
            return x_next

        x = x_next  # Atualiza x para a próxima iteração

    raise Exception("O método não convergiu após o número máximo de iterações.")

def secant_method(func, tolerance=1e-5, max_iterations=100):
    
    lambda_func = parse_expression_to_lambda(func)
    x0, x1 = find_initial_guesses(lambda_func)
    
    for i in range(max_iterations):


        f_x0 = lambda_func(x0)
        f_x1 = lambda_func(x1)

        # Evita divisão por zero na diferença
        if abs(f_x1 - f_x0) < tolerance:
            raise Exception("Diferença próxima de zero. O método não convergiu.")

        # Calcula a próxima aproximação de x usando o método da secante
        x_next = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)

        # Verifica a convergência
        if abs(x_next - x1) < tolerance:
            return x_next

        # Atualiza os pontos x0 e x1 para a próxima iteração
        x0, x1 = x1, x_next

    raise Exception("O método não convergiu após o número máximo de iterações.")
