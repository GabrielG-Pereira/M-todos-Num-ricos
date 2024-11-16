from calc.base import *

def least_squares_linear_extrapolation(x, y, x_to_extrapolate):
    # Calcula os coeficientes a e b da linha de ajuste (intercepto e inclinação)
    x_values = np.array(x)
    y_values = np.array(y)
    n = len(x_values)
    sum_x = np.sum(x_values)
    sum_y = np.sum(y_values)
    sum_x_squared = np.sum(x_values**2)
    sum_xy = np.sum(x_values * y_values)
    
    b = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x**2)
    a = (sum_y - b * sum_x) / n
    
    # Define a função de ajuste linear
    linear_func = lambda x: a + b * x
    
    # Extrapola o valor para o ponto x_to_extrapolate
    extrapolated_value = linear_func(x_to_extrapolate)
    
    return extrapolated_value, a, b