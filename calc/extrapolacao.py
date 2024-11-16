from calc.base import *

def least_squares_quadratic_extrapolation(points):
    # Extrair os valores de x e y
    x_values = np.array([p[0] for p in points])
    y_values = np.array([p[1] for p in points])
    
    # Calcular os somatórios necessários
    n = len(x_values)
    sum_x = np.sum(x_values)
    sum_y = np.sum(y_values)
    sum_x2 = np.sum(x_values**2)
    sum_x3 = np.sum(x_values**3)
    sum_x4 = np.sum(x_values**4)
    sum_xy = np.sum(x_values * y_values)
    sum_x2y = np.sum((x_values**2) * y_values)
    
    # Construir o sistema de equações
    A = np.array([
        [sum_x2, sum_x, n],
        [sum_x3, sum_x2, sum_x],
        [sum_x4, sum_x3, sum_x2]
    ])
    
    B = np.array([sum_y, sum_xy, sum_x2y])
    
    # Resolver o sistema para obter os coeficientes a, b, c
    coeffs = np.linalg.solve(A, B)
    a, b, c = coeffs
    
    # Criar a função ajustada
    def quadratic_function(x):
        return a * x**2 + b * x + c
    
    # Retornar os resultados
    return {
        "formula": f"f(x) = {a:.4f}x^2 + {b:.4f}x + {c:.4f}",
        "coefficients": {"a": a, "b": b, "c": c},
        "function": quadratic_function
    }