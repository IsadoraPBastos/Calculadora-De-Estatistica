// Funções para abrir e fechar modais
function abrirModalDiscreto() {
  document.getElementById("container_modal_discreto").classList.add("show");
  document.querySelector(".botoes-calcular-limpar").classList.add("descer");
  document.querySelector(".container-opcoes-tipo-dado").classList.add("descer");
  document.getElementById("container_modal_vac").classList.remove("show");

  // Desabilitar moda de Czuber para dados desordenados
  const modaCzuber = document.getElementById("modaCzuber");
  const modaCzuberLabel = document.querySelector('label[for="modaCzuber"]');
  modaCzuber.disabled = true;
  modaCzuber.checked = false;
  modaCzuberLabel.classList.add("disabled");
}

function fecharModalDiscreto() {
  document.getElementById("container_modal_discreto").classList.remove("show");
  document.querySelector(".botoes-calcular-limpar").classList.remove("descer");
  document
    .querySelector(".container-opcoes-tipo-dado")
    .classList.remove("descer");
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
  document
    .querySelector(".container-opcoes-tipo-dado")
    .classList.remove("descer");
}

function abrirModalVAC() {
  document.getElementById("container_modal_vac").classList.add("show");
  document.querySelector(".botoes-calcular-limpar").classList.add("descer");
  document.querySelector(".container-opcoes-tipo-dado").classList.add("descer");
}

function fecharModalVAC() {
  document.getElementById("container_modal_vac").classList.remove("show");
  document.querySelector(".botoes-calcular-limpar").classList.remove("descer");
  document
    .querySelector(".container-opcoes-tipo-dado")
    .classList.remove("descer");
}

function abrirModalVAD() {
  document.getElementById("container_modal_vad").classList.add("show");
  document.querySelector(".botoes-calcular-limpar").classList.add("descer");
  document.querySelector(".container-opcoes-tipo-dado").classList.add("descer");
}

function fecharModalVAD() {
  document.getElementById("container_modal_vad").classList.remove("show");
  document.querySelector(".botoes-calcular-limpar").classList.remove("descer");
  document
    .querySelector(".container-opcoes-tipo-dado")
    .classList.remove("descer");
}

// Seleção dos botões dentro dos modais

const secaoDadosDesordenado = document.getElementById("secaoDadosDesordenados");
const secaoDadosEmTabela = document.getElementById("secaoDadosEmTabela");

function mostrarDadosDesordenados() {
  secaoDadosDesordenado.style.display = "flex";
  secaoDadosEmTabela.style.display = "none";

  document.getElementById("btn-escolha-desordenado").classList.add("ativo");
  document.getElementById("btn-escolha-tabela").classList.remove("ativo");

  setTimeout(() => {
    const input = document.getElementById("inputAdicionarDesordenados");
    if (input) {
      input.focus();
    }
  }, 100);
}

function mostrarDadosEmTabela() {
  secaoDadosEmTabela.style.display = "flex";
  secaoDadosDesordenado.style.display = "none";

  document.getElementById("btn-escolha-desordenado").classList.remove("ativo");
  document.getElementById("btn-escolha-tabela").classList.add("ativo");

  setTimeout(() => {
    const input = document.querySelector('input[name="amostra"]');
    if (input) {
      input.focus();
    }
  }, 100);
}

const secaoDUnifor = document.getElementById("secaoDUnifor");
const secaoDExpo = document.getElementById("secaoDExpo");
const secaoDNormal = document.getElementById("secaoDNormal");

function mostrarDUnifor() {
  secaoDUnifor.style.display = "flex";
  secaoDExpo.style.display = "none";
  secaoDNormal.style.display = "none";

  document.getElementById("btn-escolha-uniforme").classList.add("ativo");
  document.getElementById("btn-escolha-exponecial").classList.remove("ativo");
  document.getElementById("btn-escolha-normal").classList.remove("ativo");
}

function mostrarDExpo() {
  secaoDExpo.style.display = "flex";
  secaoDUnifor.style.display = "none";
  secaoDNormal.style.display = "none";

  document.getElementById("btn-escolha-exponecial").classList.add("ativo");
  document.getElementById("btn-escolha-uniforme").classList.remove("ativo");
  document.getElementById("btn-escolha-normal").classList.remove("ativo");
}

function mostrarDNormal() {
  secaoDExpo.style.display = "none";
  secaoDUnifor.style.display = "none";
  secaoDNormal.style.display = "flex";

  document.getElementById("btn-escolha-exponecial").classList.remove("ativo");
  document.getElementById("btn-escolha-uniforme").classList.remove("ativo");
  document.getElementById("btn-escolha-normal").classList.add("ativo");
}

const secaoDBino = document.getElementById("secaoDBino");
const secaoDPois = document.getElementById("secaoDPois");

function mostrarDBino() {
  secaoDBino.style.display = "flex";
  secaoDPois.style.display = "none";

  document.getElementById("btn-escolha-binomial").classList.add("ativo");
  document.getElementById("btn-escolha-poisson").classList.remove("ativo");
}

function mostrarDPois() {
  secaoDPois.style.display = "flex";
  secaoDBino.style.display = "none";

  document.getElementById("btn-escolha-poisson").classList.add("ativo");
  document.getElementById("btn-escolha-binomial").classList.remove("ativo");
}

const secaoDNormal_Amostral = document.getElementById("secaoDNormal_Amostral");
const secaoDNormal_Final = document.getElementById("secaoDNormal_Final");

function mostrarDNormal_Amostral() {
  secaoDNormal_Final.style.display = "none";
  if (secaoDNormal_Amostral.style.display == "flex") {
    secaoDNormal_Amostral.style.display = "none";
  } else {
    secaoDNormal_Amostral.style.display = "flex";
  }
}


function mostrarDNormal_Final() {
  secaoDNormal_Amostral.style.display = "none";
  secaoDNormal_Final.style.display = "flex";
}

// Cards
let cardDiscreto = document.querySelector(".container-card-discreto");
let cardClasses = document.querySelector(".container-card-classes");
let cardVAC = document.querySelector(".container-card-vac");
let cardVAD = document.querySelector(".container-card-vad");
let cardEQ1 = document.querySelector(".container-card-eq1");

function paramEsta() {
  document.getElementById("btn-par-estatisticos").classList.add("ativo");
  document.getElementById("btn-probabilidade").classList.remove("ativo");
  document.getElementById("btn-reg-linear").classList.remove("ativo");

  cardVAC.style.display = "none";
  cardVAC.style.opacity = 0;
  cardVAD.style.display = "none";
  cardVAD.style.opacity = 0;
  cardEQ1.style.display = "none";
  cardEQ1.style.opacity = 0;

  cardDiscreto.style.display = "block";
  requestAnimationFrame(() => {
    cardDiscreto.style.opacity = 1;
  });

  cardClasses.style.display = "block";
  requestAnimationFrame(() => {
    cardClasses.style.opacity = 1;
  });
}

function probabilidade() {
  document.getElementById("btn-par-estatisticos").classList.remove("ativo");
  document.getElementById("btn-probabilidade").classList.add("ativo");
  document.getElementById("btn-reg-linear").classList.remove("ativo");

  cardDiscreto.style.display = "none";
  cardDiscreto.style.opacity = 0;
  cardClasses.style.display = "none";
  cardClasses.style.opacity = 0;
  cardEQ1.style.display = "none";
  cardEQ1.style.opacity = 0;

  cardVAC.style.display = "block";
  requestAnimationFrame(() => {
    cardVAC.style.opacity = 1;
  });

  cardVAD.style.display = "block";
  requestAnimationFrame(() => {
    cardVAD.style.opacity = 1;
  });
}

function regreLinear() {
  document.getElementById("btn-par-estatisticos").classList.remove("ativo");
  document.getElementById("btn-probabilidade").classList.remove("ativo");
  document.getElementById("btn-reg-linear").classList.add("ativo");

  cardDiscreto.style.display = "none";
  cardDiscreto.style.opacity = 0;
  cardClasses.style.display = "none";
  cardClasses.style.opacity = 0;
  cardVAC.style.display = "none";
  cardVAC.style.opacity = 0;
  cardVAD.style.display = "none";
  cardVAD.style.opacity = 0;

  cardEQ1.style.display = "block";
  requestAnimationFrame(() => {
    cardEQ1.style.opacity = 1;
  });
}
