from calc.base import *

def compound_trace_method(func, a, b, n):

    f = parse_expression_to_lambda(func)
    h = (b - a) / n
    soma = 0.5 * (f(a) + f(b))
    
    for i in range(1, n):
        soma += f(a + i * h)
    
    integral = h * soma
    return integral
