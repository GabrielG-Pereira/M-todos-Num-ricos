from calc.base import *

def lagrange_interpolating_polynomial(points):
    # Define a variável simbólica x
    x = sp.symbols('x')
    
    # Calcula o polinômio de Lagrange
    n = len(points)
    L = 0
    for i in range(n):
        xi, yi = points[i]
        
        # Calcula l_i(x) para o ponto (xi, yi)
        li = 1
        for j in range(n):
            if j != i:
                xj = points[j][0]
                li *= (x - xj) / (xi - xj)
        
        # Adiciona o termo yi * li ao polinômio interpolador
        L += yi * li

    # Simplifica o polinômio final
    L = sp.expand(L)
    lagrange_func = sp.lambdify(sp.symbols('x'), L, 'numpy')
    return L, lagrange_func

def newton_gregory_forward(x_values, y_values, x_to_interpolate):
    n = len(x_values)
    h = x_values[1] - x_values[0]  # Assumindo espaçamento igual
    difference_table = np.zeros((n, n))
    difference_table[:,0] = y_values
    
    # Calcula a tabela de diferenças finitas
    for i in range(1, n):
        for j in range(n - i):
            difference_table[j][i] = difference_table[j+1][i-1] - difference_table[j][i-1]
    
    # Calcula u
    x0 = x_values[0]
    u = (x_to_interpolate - x0) / h
    
    # Calcula o polinômio interpolador
    interpolated_value = y_values[0]
    u_term = 1
    factorial = 1
    for i in range(1, n):
        u_term *= (u - (i - 1))
        factorial *= i
        delta_y = difference_table[0][i]
        interpolated_value += (u_term * delta_y) / factorial
    
    return interpolated_value

def least_squares_linear(x, y):
    
    # Calcula os somatórios necessários
    x_values = np.array(x)
    y_values = np.array(y)
    
    n = len(x_values)

    sum_x = np.sum(x_values)
    sum_y = np.sum(y_values)
    sum_x_squared = np.sum(x_values**2)
    sum_xy = np.sum(x_values * y_values)
    
    # Calcula os coeficientes a e b
    b = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x**2)
    a = (sum_y - b * sum_x) / n
    
    # Retorna a função linear estimada
    return lambda x: a + b * x, a, b

