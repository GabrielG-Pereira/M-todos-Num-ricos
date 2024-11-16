
# Exemplos de uso

---

## Equações Lineares 
### Teorema de Bolzano
    Exemplo:
    - In - Expressão: x^2 - 1 = 0
    - Out - Resultado (intervalos): [(-1.2, -1.0), (0.8, 1.0)]

### Método da Bissecção
    Exemplo:
    - In - Expressão: x^2 - 1 = 0
    - Out - Resultado (raizes): [-1.0, 1.0]

### Método de Newton-Raphson 
    Exemplo:
    - In - Expressão: x^2 - 1 = 0
    - Out - Resultado (raizes): [-1.0, 1.0]

### Método da Secante
    Exemplo:
    - In - Expressão: x^2 - 1 = 0
    - Out - Resultado (raizes): [-1.0, 1.0]

---

## Sistemas Lineares 
### Eliminação de Gauss
    Exemplo:
    - In - Expressões: "4*x - y + z = 8", "-x + 3*y - z = -11", "x - y + 5*z = 3"
    - Out - Resultado: (x1) x: 1.24, (x2) y: -3.36, (x3) z: -0.31

### Método de Gauss-Jacobi
    Exemplo:
    - In - Expressões: "4*x - y + z = 8", "-x + 3*y - z = -11", "x - y + 5*z = 3"
    - Out - Resultado: x: 1.2399977827299498, y: -3.359997334132236, z: -0.3200018979453132

### Métodos iterativos
    Exemplo:
    - In - Expressões: "4*x - y + z = 8", "-x + 3*y - z = -11", "x - y + 5*z = 3"
    - Out - Resultado: x: 1.24, y: -3.36, z: -0.32

### Método de Gauss-Seidel
    Exemplo:
    - In - Expressões: "4*x - y + z = 8", "-x + 3*y - z = -11", "x - y + 5*z = 3"
    - Out - Resultado: x: 1.2400001187917953, y: -3.3599997423557526, z: -0.31999997222950965

---

## Interpolação 
### Interpolação Lagrange
    Exemplo:
    - In - Pontos: "(1, 2), (2, 3), (3, 5)"
    - Out – Resultado: 0.5*x**2 - 0.5*x + 2.0

### Interpolação Newton-Gregory
    Exemplo:
    - In - Valor de X: 1, 2, 3, 4, 5
    - In - Valor de Y: 2, 3, 5, 7, 11
    - In - Valor da Interpolação: 6
    - Out – Resultado: 22

### Interpolação Inversa
    Exemplo:
    - In - Valor de X: 1, 2, 3, 4, 5
    - In - Valor de Y: 2, 3, 5, 7, 11
    - Out - Resultado: y = -1.000000 + 2.200000x

---

## Extrapolação 
### Método dos mínimos quadrados
    Exemplo:
    - In - Pontos: (1, 2), (2, 3), (3, 5)
    - Out - Função: f(x) = 0.5000x^2 + -0.5000x + 2.0000 | Coeficientes: a: 0.5, b: -0.5, c: 2.0

---

## Integração
### Método do Trapézio Composto
    Exemplo:
    - In - Expressão: x**2 + 2*x + 1
    - In - Valor de A: 0
    - In - Valor de B: 1
    - In - Valor da Integração: 10
    - Out - Resultado: 2.3353909465020575