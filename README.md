# Exemplos de Uso 📘

Este repositório contém exemplos práticos de **métodos numéricos** aplicados em diversas áreas, como solução de equações, sistemas lineares, interpolação, extrapolação e integração. Esses métodos são amplamente usados em problemas de engenharia, física, matemática e computação para resolver desafios complexos de forma eficiente e precisa.

---

## ✨ Resumo

Neste documento, você encontrará:
- **Equações Lineares**: Métodos como o **Teorema de Bolzano**, **Bissecção**, **Newton-Raphson** e **Secante** para encontrar raízes de equações não lineares.
- **Sistemas Lineares**: Soluções com **Eliminação de Gauss**, **Gauss-Jacobi**, **Gauss-Seidel** e métodos iterativos para resolver sistemas de equações lineares.
- **Interpolação**: Técnicas como **Lagrange**, **Newton-Gregory** e **Interpolação Inversa** para estimar valores intermediários em conjuntos de dados.
- **Extrapolação**: Aplicação do **Método dos Mínimos Quadrados** para prever tendências e ajustar curvas.
- **Integração**: Uso do **Método do Trapézio Composto** para calcular aproximações numéricas de integrais definidas.

Cada seção inclui exemplos detalhados de entrada e saída para facilitar a compreensão e a aplicação dos métodos.

---

## 📐 Equações Lineares

### 🔹 **Teorema de Bolzano**
- **Entrada**:  
  - Expressão: `x^2 - 1 = 0`
- **Saída**:  
  - Intervalos: `[(-1.2, -1.0), (0.8, 1.0)]`

---

### 🔹 **Método da Bissecção**
- **Entrada**:  
  - Expressão: `x^2 - 1 = 0`
- **Saída**:  
  - Raízes: `[-1.0, 1.0]`

---

### 🔹 **Método de Newton-Raphson**
- **Entrada**:  
  - Expressão: `x^2 - 1 = 0`
- **Saída**:  
  - Raízes: `[-1.0, 1.0]`

---

### 🔹 **Método da Secante**
- **Entrada**:  
  - Expressão: `x^2 - 1 = 0`
- **Saída**:  
  - Raízes: `[-1.0, 1.0]`

---

## 🧮 Sistemas Lineares

### 🔹 **Eliminação de Gauss**
- **Entrada**:  
  - Expressões:  
    ```
    4*x - y + z = 8  
    -x + 3*y - z = -11  
    x - y + 5*z = 3
    ```
- **Saída**:  
  - (x1) `x: 1.24`, (x2) `y: -3.36`, (x3) `z: -0.31`

---

### 🔹 **Método de Gauss-Jacobi**
- **Entrada**:  
  - Expressões:  
    ```
    4*x - y + z = 8  
    -x + 3*y - z = -11  
    x - y + 5*z = 3
    ```
- **Saída**:  
  - `x: 1.2399977827299498`, `y: -3.359997334132236`, `z: -0.3200018979453132`

---

### 🔹 **Métodos Iterativos**
- **Entrada**:  
  - Expressões:  
    ```
    4*x - y + z = 8  
    -x + 3*y - z = -11  
    x - y + 5*z = 3
    ```
- **Saída**:  
  - `x: 1.24`, `y: -3.36`, `z: -0.32`

---

### 🔹 **Método de Gauss-Seidel**
- **Entrada**:  
  - Expressões:  
    ```
    4*x - y + z = 8  
    -x + 3*y - z = -11  
    x - y + 5*z = 3
    ```
- **Saída**:  
  - `x: 1.2400001187917953`, `y: -3.3599997423557526`, `z: -0.31999997222950965`

---

## 📊 Interpolação

### 🔹 **Interpolação de Lagrange**
- **Entrada**:  
  - Pontos: `(1, 2), (2, 3), (3, 5)`
- **Saída**:  
  - Função: `0.5*x^2 - 0.5*x + 2.0`

---

### 🔹 **Interpolação de Newton-Gregory**
- **Entrada**:  
  - Valores de X: `1, 2, 3, 4, 5`  
  - Valores de Y: `2, 3, 5, 7, 11`  
  - Valor da Interpolação: `6`
- **Saída**:  
  - Resultado: `22`

---

### 🔹 **Interpolação Inversa**
- **Entrada**:  
  - Valores de X: `1, 2, 3, 4, 5`  
  - Valores de Y: `2, 3, 5, 7, 11`
- **Saída**:  
  - Função: `y = -1.000000 + 2.200000x`

---

## 📈 Extrapolação

### 🔹 **Método dos Mínimos Quadrados**
- **Entrada**:  
  - Pontos: `(1, 2), (2, 3), (3, 5)`
- **Saída**:  
  - Função: `f(x) = 0.5000x^2 - 0.5000x + 2.0000`  
  - Coeficientes: `a: 0.5`, `b: -0.5`, `c: 2.0`

---

## ∫ Integração

### 🔹 **Método do Trapézio Composto**
- **Entrada**:  
  - Expressão: `x**2 + 2*x + 1`  
  - Valor de A: `0`  
  - Valor de B: `1`  
  - Valor da Integração: `10`
- **Saída**:  
  - Resultado: `2.3353909465020575`

---

## 🚀 Contribua!
Se tiver sugestões ou encontrar problemas, sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_. 💡