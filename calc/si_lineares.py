from calc.base import *

def newton_method_system(funcs, variables, initial_guess=None, tolerance=1e-5, max_iterations=100):
    
    # Converte as expressões para funções lambda
    functions = [parse_expression_to_lambda(expr, variables) for expr in funcs]

    # Deriva as funções para obter a Jacobiana
    jacobian = derive_jacobian_matrix(functions, variables)

    # Define o chute inicial
    if initial_guess is None:
        initial_guess = [1.0] * len(variables)  # Chute inicial padrão com 1.0 para cada variável

    # Converte o chute inicial para um array numpy
    x = np.array(initial_guess, dtype=float)

    for iteration in range(max_iterations):
        # Avalia as funções no ponto atual
        F = np.array([f(*x) for f in functions], dtype=float)

        # Avalia a Jacobiana no ponto atual
        try:
            J = np.array([[df(*x) for df in row] for row in jacobian], dtype=float)
            # Resolve o sistema linear J * delta = -F para encontrar o ajuste delta
            delta = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            raise Exception("A Jacobiana é singular ou próxima de ser singular; o método não pode continuar.")
            return None

        # Atualiza a aproximação
        x = x + delta

        # Verifica a convergência
        if np.linalg.norm(delta, ord=np.inf) < tolerance:
            print(f"Convergiu em {iteration + 1} iterações.")
            return str(", ".join(f"{var}: {float(valor)}" for var, valor in dict(zip(variables, x)).items()))

    raise Exception("O método não convergiu após o número máximo de iterações.")

def gauss_elimination_from_expressions(expressions, variables):
    # Define os símbolos para as variáveis
    symbols = sp.symbols(variables)

    # Converte as expressões em objetos simbólicos e calcula os coeficientes e termos independentes
    A = []
    b = []
    for expr in expressions:
        # Remove o '=' e transforma em uma expressão simbólica
        if '=' in expr:
            left, right = expr.split('=')
            sympy_expr = sp.sympify(f"({left}) - ({right})".replace("^", "**"))
        else:
            sympy_expr = sp.sympify(expr.replace("^", "**"))
        
        # Extrai os coeficientes e o termo independente
        row = [sympy_expr.coeff(var) for var in symbols]
        const_term = -sympy_expr.subs({var: 0 for var in symbols})
        
        A.append(row)
        b.append(const_term)

    # Converte A e b para arrays numpy
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)

    # Eliminação Gaussiana
    for i in range(n):
        # Pivoteamento: troca de linhas se o elemento pivô é zero
        if A[i, i] == 0:
            for k in range(i + 1, n):
                if A[k, i] != 0:
                    A[[i, k]] = A[[k, i]]
                    b[[i, k]] = b[[k, i]]
                    break
            else:
                raise ValueError("O sistema não tem solução única ou a matriz é singular.")

        # Normaliza a linha do pivô
        for j in range(i + 1, n):
            factor = A[j, i] / A[i, i]
            A[j, i:] = A[j, i:] - factor * A[i, i:]
            b[j] = b[j] - factor * b[i]

    # Substituição Reversa para obter a solução
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]

    return str(", ".join(f"{var}: {float(valor)}" for var, valor in dict(zip(variables, x)).items()))

def gauss_jacobi_from_expressions(equations, variables, tolerance=1e-5, max_iterations=100):
    # Define os símbolos para as variáveis
    symbols = sp.symbols(variables)

    # Converte as expressões em funções e calcula os coeficientes e termos independentes
    A = []
    b = []
    for expr in equations:
        # Divide a expressão em esquerda e direita do sinal de igualdade
        if '=' in expr:
            left, right = expr.split('=')
            sym_expr = sp.sympify(f"({left}) - ({right})")
        else:
            sym_expr = sp.sympify(expr)

        # Extrai os coeficientes e o termo independente
        row = [sym_expr.coeff(var) for var in symbols]
        const_term = -sym_expr.subs({var: 0 for var in symbols})
        
        A.append(row)
        b.append(const_term)

    # Converte A e b para arrays numpy
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)

    # Inicialização das variáveis de solução
    x = np.zeros(n)
    x_new = np.zeros(n)

    # Método de Gauss-Jacobi
    for iteration in range(max_iterations):
        for i in range(n):
            # Calcula a soma excluindo o termo da diagonal
            sum_j = sum(A[i, j] * x[j] for j in range(n) if j != i)
            # Atualiza a variável i considerando apenas os valores da iteração anterior
            x_new[i] = (b[i] - sum_j) / A[i, i]

        # Verifica a convergência com base na norma das diferenças
        if np.linalg.norm(x_new - x, ord=np.inf) < tolerance:
            print(f"Convergiu em {iteration + 1} iterações.")
            return str(", ".join(f"{var}: {float(valor)}" for var, valor in dict(zip(variables, x_new)).items()))


        # Atualiza x para a próxima iteração
        x = x_new.copy()

    raise Exception("O método não convergiu após o número máximo de iterações.")


def gauss_seidel_from_expressions(equations, variables, tolerance=1e-5, max_iterations=100):
    # Define os símbolos para as variáveis
    symbols = sp.symbols(variables)

    # Converte as expressões em funções e calcula os coeficientes e termos independentes
    A = []
    b = []
    for expr in equations:
        # Divide a expressão em esquerda e direita do sinal de igualdade
        if '=' in expr:
            left, right = expr.split('=')
            sym_expr = sp.sympify(f"({left}) - ({right})")
        else:
            sym_expr = sp.sympify(expr)

        # Extrai os coeficientes e o termo independente
        row = [sym_expr.coeff(var) for var in symbols]
        const_term = -sym_expr.subs({var: 0 for var in symbols})
        
        A.append(row)
        b.append(const_term)

    # Converte A e b para arrays numpy
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)

    # Inicialização das variáveis de solução
    x = np.zeros(n)

    # Método de Gauss-Seidel
    for iteration in range(max_iterations):
        x_old = x.copy()
        for i in range(n):
            # Calcula a soma excluindo o termo da diagonal
            sum_j = sum(A[i, j] * x[j] for j in range(n) if j != i)
            # Atualiza a variável i usando o valor atualizado de x
            x[i] = (b[i] - sum_j) / A[i, i]

        # Verifica a convergência com base na norma das diferenças
        if np.linalg.norm(x - x_old, ord=np.inf) < tolerance:
            print(f"Convergiu em {iteration + 1} iterações.")
            return str(", ".join(f"{var}: {float(valor)}" for var, valor in dict(zip(variables, x)).items()))

    raise Exception("O método não convergiu após o número máximo de iterações.")
