const container_modal_desordenado = document.getElementById('container_modal_desordenado');
const container_modal_tabela = document.getElementById('container_modal_tabela');
const container_modal_classes = document.getElementById('container_modal_classes');
const botoes = document.querySelector('.botoes-calcular-limpar');
const tipo_dado = document.querySelector(".container-opcoes-tipo-dado");


function abrirModalDesordenado() {
    container_modal_desordenado.classList.add('show');
    botoes.classList.add('descer');
    tipo_dado.classList.add("descer");
}
    
function fecharModalDesordenado() {
    container_modal_desordenado.classList.remove('show');
    botoes.classList.remove('descer');
    tipo_dado.classList.remove("descer");
}

function abrirModalTabela() {
    container_modal_tabela.classList.add('show');
    botoes.classList.add('descer');
    tipo_dado.classList.add("descer");
}
    
function fecharModalTabela() {
    container_modal_tabela.classList.remove('show');
    botoes.classList.remove('descer');
    tipo_dado.classList.remove("descer");
}

function abrirModalClasses() {
    container_modal_classes.classList.add('show');
    botoes.classList.add('descer');
    tipo_dado.classList.add("descer");
}

function fecharModalClasses(){
    container_modal_classes.classList.remove('show');
    botoes.classList.remove('descer');
    tipo_dado.classList.remove("descer");
}
   
