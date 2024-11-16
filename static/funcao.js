const subgruposOptions = {
    "equacoes-lineares": ["Teorema de Bolzano", "Método da Bissecção", "Método de Newton-Raphson", "Método da Secante"],
    "sistemas-lineares": ["Eliminação de Gauss", "Método de Gauss-Jacobi", "Metodos iterativos", "Método de Gauss-Seidel"],
    "interpolacao": ["Interpolação Lagrange", "Interpolação Newton-Gregory", "Interpolação Inversa"],
    "extrapolacao": ["Método dos mínimos quadrados"],
    "integracao": ["Método do Trapezio Composto"]
};

function updateSubgrupos() {
    const grupoSelecionado = document.getElementById('grupos').value;
    const subgruposSelect = document.getElementById('subgrupos');

    subgruposSelect.innerHTML = '<option value="">Selecionar</option>';

    if (grupoSelecionado && subgruposOptions[grupoSelecionado]) {
        subgruposOptions[grupoSelecionado].forEach(subgrupo => {
            const option = document.createElement('option');
            option.value = subgrupo.toLowerCase().replace(/\s+/g, '-');
            option.textContent = subgrupo;
            subgruposSelect.appendChild(option);
        });
    }
    atualizarCampos()
}

function atualizarCampos() {
    // Obtem o grupo e subgrupo selecionados
    const grupoSelecionado = document.getElementById('grupos').value;
    const subgrupoSelecionado = document.getElementById('subgrupos').value;
    const subgrupo = document.getElementById('subgrup');

    // Elementos a serem manipulados
    const expressao = document.getElementById('expressao');
    const pontos = document.getElementById('pontos');
    const x = document.getElementById('x');
    const y = document.getElementById('y');
    const valor = document.getElementById('valor');
    const calculate = document.getElementById('calculate');
    const resultado = document.getElementById('resultado');
    const botaoExpressao = document.getElementById('botao-expressao');

    // Oculta todos os campos inicialmente
    expressao.style.display = 'none';
    pontos.style.display = 'none';
    x.style.display = 'none';
    y.style.display = 'none';
    valor.style.display = 'none';
    calculate.style.display = 'none';
    resultado.style.display = 'none';

    // Lógica de visibilidade com base no grupo e subgrupo selecionado
    if (grupoSelecionado === 'equacoes-lineares'){
        botaoExpressao.style.display = 'none';
        removeAllExpressionFields();
    } else{
        botaoExpressao.style.display = 'block';
    }

    if (grupoSelecionado === 'equacoes-lineares' || grupoSelecionado === 'sistemas-lineares') {
        expressao.style.display = 'block';
        calculate.style.display = 'block';
        resultado.style.display = 'block';
    } else if (subgrupoSelecionado === 'interpolação-lagrange' || subgrupoSelecionado === 'método-dos-mínimos-quadrados') {
        pontos.style.display = 'block';
        calculate.style.display = 'block';
        resultado.style.display = 'block';
    } else if (subgrupoSelecionado === 'interpolação-inversa') {
        x.style.display = 'block';
        y.style.display = 'block';
        calculate.style.display = 'block';
        resultado.style.display = 'block';
    } else if (subgrupoSelecionado === 'interpolação-newton-gregory') {
        x.style.display = 'block';
        y.style.display = 'block';
        valor.style.display = 'block';
        calculate.style.display = 'block';
        resultado.style.display = 'block';
    } else if (grupoSelecionado === 'integracao'){
        expressao.style.display = 'block';
        x.style.display = 'block';
        y.style.display = 'block';
        valor.style.display = 'block';
        calculate.style.display = 'block';
        resultado.style.display = 'block';
    } 

    if(grupoSelecionado === ''){
        subgrupo.style.display = 'none';
    } else{
        subgrupo.style.display = 'block';
    }

    if (subgrupoSelecionado === ''){
        expressao.style.display = 'none';
        pontos.style.display = 'none';
        x.style.display = 'none';
        y.style.display = 'none';
        valor.style.display = 'none';
        calculate.style.display = 'none';
        resultado.style.display = 'none';
    }
    document.getElementById("result").textContent = '';
    
}

async function validateAndSendFunction() {
    const subgrupo = document.getElementById('subgrupos').value;
    
    // Seleciona todos os elementos com o ID 'exp' e obtém seus valores
    const expElements = document.querySelectorAll('.exp');
    const expressao = Array.from(expElements).map(element => element.value);

    const pontos = document.getElementById('pon').value;
    const x = document.getElementById('xp').value;
    const y = document.getElementById('yp').value;
    const valor = document.getElementById('val').value;

    const dados = {
        subgrupo,
        expressao,  // Passa a lista de valores de 'exp' como a propriedade expressao
        pontos,
        x,
        y,
        valor
    };

    try {
        document.getElementById("result").textContent = "Calculando...";
        // Envia a requisição POST para o servidor
        const response = await fetch('/processar_dados', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        // Verifica se a resposta é bem-sucedida
        if (!response.ok) {
            throw new Error('Erro ao enviar os dados');
        }

        // Processa a resposta do servidor
        const resultado = await response.json();
        console.log("Resultado do servidor:", resultado);

        document.getElementById("result").textContent = resultado["result"];
    } catch (error) {
        console.error('Erro:', error);
    }
}


// todas as funções de metodos

let fieldIdCounter = 0; // Contador global para IDs únicos

// Função para adicionar uma nova div com ID único
function addExpressionField() {
    const additionalExpressions = document.getElementById('additionalExpressions');
    const newField = document.createElement('div');
    const uniqueId = `expression-field-${fieldIdCounter++}`; // Gera um ID único
    newField.setAttribute('id', uniqueId); // Atribui o ID à div
    newField.classList.add('input-group');
    newField.innerHTML = `
        <input type="text" class="exp" name="expression" placeholder="e.g., x^2 * 4 y = 0">
        <button type="button" onclick="removeExpressionField('${uniqueId}')">-</button>
    `;
    additionalExpressions.appendChild(newField);
}

// Função para remover uma div específica
function removeExpressionField(id) {
    const field = document.getElementById(id);
    if (field) {
        field.remove();
    }
}

// Função para remover todas as divs criadas
function removeAllExpressionFields() {
    const additionalExpressions = document.getElementById('additionalExpressions');
    additionalExpressions.innerHTML = ''; // Remove todo o conteúdo
    fieldIdCounter = 0; // Reseta o contador de IDs
}

function removeExpressionField(button) {
    const fieldToRemove = button.parentElement;
    fieldToRemove.remove();
}

async function buscarTexto() {
    try {
        // Realiza a requisição GET para a rota '/obter_texto'
        const response = await fetch('/obter_texto');

        // Verifica se a resposta é bem-sucedida
        if (!response.ok) {
            throw new Error('Erro ao buscar o texto');
        }

        // Converte a resposta para JSON
        const data = await response.json();

        // Atualiza o elemento 'grupos' com o grupo retornado
        document.getElementById('grupos').value = data.grup;

        // Chama a função para atualizar os subgrupos com base no grupo selecionado
        updateSubgrupos();

        // Seleciona o subgrupo específico no 'subgrupos'
        const subgruposSelect = document.getElementById('subgrupos');
        const subgrupoValue = data.item.toLowerCase().replace(/\s+/g, '-');
        for (const option of subgruposSelect.options) {
            if (option.value === subgrupoValue) {
                option.selected = true;
                break;
            }
        }
        atualizarCampos()

        // Exibe um alerta com o grupo e subgrupo selecionados (opcional)
    } catch (error) {
        alert('Erro: ' + error);
    }
}
