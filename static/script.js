// Funções para abrir e fechar modais
function abrirModalDiscreto() {
  document.getElementById("container_modal_discreto").classList.add("show");
  document.querySelector(".botoes-calcular-limpar").classList.add("descer");
  document.querySelector(".container-opcoes-tipo-dado").classList.add("descer");
  
  // Desabilitar moda de Czuber para dados desordenados
  const modaCzuber = document.getElementById("modaCzuber");
  const modaCzuberLabel = document.querySelector('label[for="modaCzuber"]');
  modaCzuber.disabled = true;
  modaCzuber.checked = false;
  modaCzuberLabel.classList.add("disabled");
}

function abrirModalDiscreto() {
  document.getElementById("container_modal_discreto").classList.remove("show");
  document.querySelector(".botoes-calcular-limpar").classList.remove("descer");
  document.querySelector(".container-opcoes-tipo-dado").classList.remove("descer");
}

function abrirModalClasses() {
  document.getElementById("container_modal_classes").classList.add("show");
  document.querySelector(".botoes-calcular-limpar").classList.add("descer");
  document.querySelector(".container-opcoes-tipo-dado").classList.add("descer");
  
  // Habilitar moda de Czuber para dados em classes
  const modaCzuber = document.getElementById("modaCzuber");
  const modaCzuberLabel = document.querySelector('label[for="modaCzuber"]');
  modaCzuber.disabled = false;
  modaCzuberLabel.classList.remove("disabled");
}

function fecharModalClasses() {
  document.getElementById("container_modal_classes").classList.remove("show");
  document.querySelector(".botoes-calcular-limpar").classList.remove("descer");
  document.querySelector(".container-opcoes-tipo-dado").classList.remove("descer");
}