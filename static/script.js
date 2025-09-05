const open = document.getElementById('open');
const container_modal_desordenado = document.getElementById('container_modal_desordenado');
const container_modal_tabela = document.getElementById('container_modal_tabela');
const close = document.getElementById('close');
const botoes = document.querySelector('.botoes-calcular-limpar');


function abrirModalDesordenado() {
    container_modal_desordenado.classList.add('show');
    botoes.classList.add('descer');
}
    
function fecharModalDesordenado() {
    container_modal_desordenado.classList.remove('show');
    botoes.classList.remove('descer');
}

function abrirModalTabela() {
    container_modal_tabela.classList.add('show');
    botoes.classList.add('descer');
}
    
function fecharModalTabela() {
    container_modal_tabela.classList.remove('show');
    botoes.classList.remove('descer');
}
   