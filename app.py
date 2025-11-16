# pip install flask
import json
import math
from flask import Flask, render_template, request, Response
import math
from scipy.stats import norm #pip install scipy

app = Flask(__name__)

# Definição das variáveis 
dadosDesordenados = []; FequenciaIndividualAbsolutaRecebida = {}; FequenciaIndividualAbsoluta = {}; dadosClasses = []; TabelaDeDados = {}

limiteSuperior = limiteInferior = vLambda = vMedia = desvioPadrao = 0
valorA = valorB = valorANorm = valorBNorm = probabSucesso = vTotal = valorX = valorY = valorCUnif = valorDUnif = 0
tamanhoAmostraNorm = mediaNorm = desvioPadraoNorm = intervalo = 0

reqDistNormal = secaoDNormalFinal = calcularNormal = False

moda = mediana = None


@app.route('/')
def index():
    return render_template('index.html', FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={}, 
    FequenciaIndividualAbsolutaRecebida = {}, dadosClasses=[], escolhaCalculo=[], mostrar_modal="padrao", TabelaDeDados={}, limiteSuperior=0, limiteInferior=0, vLambda=0, mostrarResultados=False)

#Recebe os dados quando a pessoa envia eles pela parte desordenada 
@app.route("/dados_desordenados", methods=["POST", "GET"])
def dados_desordenados():
    global reqDistNormal, desvioPadraoNorm, mediaNorm, tamanhoAmostraNorm, calcularNormal, valorANorm, valorBNorm, intervalo, moda, mediana
    if request.method == "POST":
        if request.form.get("dado"):
            dadosDesordenados.append(float(request.form.get("dado")))
            FequenciaIndividualAbsolutaRecebida.clear()
            FequenciaIndividualAbsoluta.clear()
            dadosClasses.clear()
        elif request.form.get("limpar") == "limpar":
            dadosDesordenados.clear()
        elif request.form.get("reqDistNormal"):
            reqDistNormal = True
    return render_template("index.html", mostrar_modal="discreto", mostrar_desor_ou_tab="desordenado", 
    dadosDesordenados=dadosDesordenados, FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={}, 
    FequenciaIndividualAbsolutaRecebida = {}, dadosClasses=[], escolhaCalculo=[],mostrarResultados=False, TabelaDeDados={},limiteSuperior=0, limiteInferior=0, reqDistNormal=reqDistNormal)

#Recebe os dados quando a pessoa envia eles pela parte de tabela
@app.route("/dados_em_tabela", methods=["POST", "GET"])
def dados_em_tabela():
    global reqDistNormal, desvioPadraoNorm, mediaNorm, tamanhoAmostraNorm, calcularNormal, valorANorm, valorBNorm, intervalo, moda, mediana
    #Organiza os dados na tabela de FI
    if request.method == "POST":
        if request.form.get("amostra" and "frequencia"):
            amostra = float(request.form.get('amostra'))
            frequencia = float(request.form.get('frequencia'))

            erroFIMenorZero = False
            if frequencia <= 0:
                erroFIMenorZero = True
            else: 
                FequenciaIndividualAbsolutaRecebida[amostra] = frequencia
                
                dadosDesordenados.clear()
                dadosClasses.clear()
        elif request.form.get("limpar"):
            amostraLimpar = request.form.get("limpar")
            FequenciaIndividualAbsolutaRecebida.pop(float(amostraLimpar))
        elif request.form.get("reqDistNormal"):
            reqDistNormal = True
    return render_template("index.html", mostrar_modal="discreto", mostrar_desor_ou_tab="tabela", 
    FequenciaIndividualAbsolutaRecebida=FequenciaIndividualAbsolutaRecebida, FequenciaIndividualAbsoluta={},
    FrequenciaAcumulada={}, Posicoes={}, dadosClasses=[], escolhaCalculo=[],mostrarResultados=False, erroFIMenorZero=erroFIMenorZero, 
    limiteSuperior=0, limiteInferior=0, reqDistNormal=reqDistNormal, TabelaDeDados = {}, NormalTabelaDeDados={})

@app.route("/agrupamento_classes", methods=["POST", "GET"])
def agrupamento_classes():
    global dadosClasses, reqDistNormal, desvioPadraoNorm, mediaNorm, tamanhoAmostraNorm, calcularNormal, valorANorm, valorBNorm, intervalo, moda, mediana
    dadosClasses.clear()
    if request.form.get("reqDistNormal"):
        reqDistNormal = True
    if request.method == "POST":
        if request.form.get("li") and request.form.get("amplitude") and request.form.get("qtd"):
            li = float(request.form.get('li'))
            amplitude = float(request.form.get('amplitude'))
            qtd = int(request.form.get('qtd'))
            
            i = 0
            while(i < qtd):
                ls = li + amplitude
                dadosClasses.append({
                    'li': li,
                    'ls': ls, 
                    'fi': 1,
                    'xi': (li + ls) / 2  
                })
                li = ls
                i += 1
            
            # Ordena por Li
            dadosClasses.sort(key=lambda x: x['li'])

            dadosDesordenados.clear()
            FequenciaIndividualAbsolutaRecebida.clear()
            FequenciaIndividualAbsoluta.clear()
            print("---------------------- dados Classes ----------------------")
            print("li", li)
            print("amplitude", amplitude)
            print("qtd", qtd)
            print("reqDistNormal", reqDistNormal)
    return render_template("index.html", mostrar_modal="classes", 
    dadosClasses=dadosClasses, modaBruta=True, FequenciaIndividualAbsolutaRecebida={}, 
    FequenciaIndividualAbsoluta={}, FrequenciaAcumulada={}, Posicoes={}, 
    escolhaCalculo=[], mostrarResultados=False,TabelaDeDados={}, limiteSuperior=0, reqDistNormal=reqDistNormal, limiteInferior=0)

@app.route("/alteração_fi", methods=["POST", "GET"])
def alteração_fi():
    global dadosClasses, reqDistNormal, desvioPadraoNorm, mediaNorm, tamanhoAmostraNorm, calcularNormal, valorANorm, valorBNorm, intervalo, moda, mediana
    if request.form.get("reqDistNormal"):
        reqDistNormal = True
    if request.method == "POST":
        erroMenorZero = False
        for i, classe in enumerate(dadosClasses):
            fi = request.form.get(f'fi_{i}')
            if int(fi) > 0:
                classe['fi'] = int(fi)
            else:
                erroMenorZero = True

        if request.form.get("limpar") == "limpar":
            dadosClasses.clear()
            

    return render_template("index.html", mostrar_modal="classes", 
    dadosClasses=dadosClasses, modaBruta=True, FequenciaIndividualAbsolutaRecebida={}, 
    FequenciaIndividualAbsoluta={}, FrequenciaAcumulada={}, Posicoes={}, 
    escolhaCalculo=[], mostrarResultados=False,TabelaDeDados={}, erroMenorZero=erroMenorZero, limiteSuperior=0, limiteInferior=0, reqDistNormal=reqDistNormal)

@app.route("/dist_uniforme", methods=["POST", "GET"])
def dist_uniforme():
    resetar_variaveis()
    global limiteSuperior, limiteInferior, valorCUnif, valorDUnif, intervalo
    if request.method == "POST":

        if request.form.get("limiteSuperior") and request.form.get("limiteInferior") and request.form.get("valorCUnif") and request.form.get("intervalo"):
            limiteSuperior = float(request.form.get('limiteSuperior'))
            limiteInferior = float(request.form.get('limiteInferior'))   
            valorCUnif = float(request.form.get("valorCUnif"))
            intervalo = request.form.get("intervalo")
            print("limiteSuperior", limiteSuperior)
            print("limiteInferior", limiteInferior)
            print("intervalo", intervalo)
            print("valorCUnif", valorCUnif)
            if request.form.get("valorDUnif") and len(intervalo) > 18:
                valorDUnif = float(request.form.get("valorDUnif"))
            else: 
                valorDUnif = 0

    return render_template("index.html", limiteSuperior=limiteSuperior, limiteInferior=limiteInferior, valorCUnif=valorCUnif, valorDUnif=valorDUnif,
    intervalo=intervalo, mostrar_modal="uniforme", dados_vac=True,
    dadosClasses={}, modaBruta=False, FequenciaIndividualAbsolutaRecebida={}, 
    FequenciaIndividualAbsoluta={}, FrequenciaAcumulada={}, Posicoes={},  TabelaDeDados={},
    escolhaCalculo=[], mostrarResultados=False)

@app.route("/dist_exponencial", methods=["POST", "GET"])
def dist_exponencial():
    resetar_variaveis()
    global vLambda, desvioPadrao, valorA, valorB, intervalo
    if request.method == "POST":
        if request.form.get("vLambda") and request.form.get("valorA") and request.form.get("intervalo"):
            vLambda = float(request.form.get('vLambda')) 
            valorA = float(request.form.get("valorA"))
            intervalo = request.form.get("intervalo")
            desvioPadrao = 0
            if request.form.get("valorB") and len(intervalo) > 18:
                 valorB = float(request.form.get("valorB"))
            else: 
                valorB = 0
        elif request.form.get("desvioPadrao") and request.form.get("valorA") and request.form.get("intervalo"):
            valorA = float(request.form.get("valorA"))    
            intervalo = request.form.get("intervalo")
            desvioPadrao = float(request.form.get("desvioPadrao"))
            vLambda = 0
            if request.form.get("valorB") and len(intervalo) > 18:
                valorB = float(request.form.get("valorB"))
                if(valorB == ""):
                    valorB = 0
            else: 
                valorB = 0

    return render_template("index.html", vLambda=vLambda, desvioPadrao=desvioPadrao, valorA=valorA, 
    valorB=valorB, intervalo=intervalo, mostrar_modal="exponencial", dados_vac=True, dadosClasses={}, modaBruta=False, 
    FequenciaIndividualAbsolutaRecebida={}, FequenciaIndividualAbsoluta={}, FrequenciaAcumulada={}, TabelaDeDados={},
    Posicoes={}, escolhaCalculo=[], mostrarResultados=False)

@app.route("/dist_normal_pad", methods=["POST", "GET"])
def dist_normal_pad():
    global desvioPadraoNorm, mediaNorm, tamanhoAmostraNorm, calcularNormal, valorANorm, valorBNorm, intervalo, moda, mediana, reqDistNormal
    if request.method == "POST":
        if request.form.get("valorANorm") and request.form.get("intervalo"):
            valorANorm = float(request.form.get('valorANorm'))      
            intervalo = request.form.get("intervalo")
            print("------------------------- dist_normal_pad -------------------------")
            if request.form.get("mediaNorm") and request.form.get("desvioPadraoNorm"):
                mediaNorm = float(request.form.get("mediaNorm"))
                desvioPadraoNorm = float(request.form.get("desvioPadraoNorm"))
                if(request.form.get("tamanhoAmostraNorm")):
                    tamanhoAmostraNorm = int(request.form.get("tamanhoAmostraNorm"))
                elif(tamanhoAmostraNorm == 0):
                    tamanhoAmostraNorm = None
            if len(intervalo) > 18:
                if(request.form.get('valorBNorm') == ""):
                    valorBNorm = 0
                else: 
                    valorBNorm = float(request.form.get('valorBNorm')) 
            else: 
                valorBNorm = 0
            print('valorBNorm', valorBNorm)
            print('valorANorm', valorANorm)
            print('mediaNorm', mediaNorm)
            print('desvioPadraoNorm', desvioPadraoNorm)
            print('tamanhoAmostraNorm', tamanhoAmostraNorm)
            if(valorANorm != 0 and mediaNorm != 0 and desvioPadraoNorm != 0 and tamanhoAmostraNorm == None):
                calcularNormal = True
                reqDistNormal = True
            
    return render_template("index.html", valorANorm=valorANorm, valorBNorm=valorBNorm,
    intervalo=intervalo, mediaNorm=mediaNorm, desvioPadraoNorm=desvioPadraoNorm, tamanhoAmostraNorm=tamanhoAmostraNorm, 
    mostrar_modal="normal", dados_vac=True, calcularNormal=calcularNormal, moda=moda, mediana=mediana,
    dadosClasses={}, modaBruta=False, FequenciaIndividualAbsolutaRecebida={}, 
    FequenciaIndividualAbsoluta={}, FrequenciaAcumulada={}, Posicoes={}, TabelaDeDados={},
    escolhaCalculo=[], mostrarResultados=False, reqDistNormal=reqDistNormal)

@app.route("/dist_binomial", methods=["POST", "GET"])
def dist_binomial():
    resetar_variaveis()
    global vTotal, probabSucesso, valorA, valorB, intervalo
    if request.method == "POST":
        if request.form.get("vTotal") and request.form.get("probabSucesso") and request.form.get("valorA") and request.form.get("intervalo"):
            vTotal = int(request.form.get("vTotal"))
            probabSucesso = float(request.form.get("probabSucesso"))
            valorA = int(request.form.get("valorA"))
            intervalo = request.form.get("intervalo")
            
            if request.form.get("valorB") and len(intervalo) > 18:
                valorB = int(request.form.get("valorB"))
            else: 
                valorB = 0
    return render_template("index.html", probabSucesso=probabSucesso, vTotal=vTotal, valorA=valorA, 
    valorB=valorB, intervalo=intervalo, mostrar_modal="binomial", dados_vac=True, dadosClasses={}, modaBruta=False, 
    FequenciaIndividualAbsolutaRecebida={}, FequenciaIndividualAbsoluta={}, FrequenciaAcumulada={}, TabelaDeDados={},
    Posicoes={}, escolhaCalculo=[], mostrarResultados=False)

@app.route("/dist_poisson", methods=["POST", "GET"])
def dist_poisson():
    resetar_variaveis()
    global vMedia, valorA, valorB, intervalo
    if request.method == "POST":
        if request.form.get("vMedia") and request.form.get("valorA") and request.form.get("intervalo"):
            vMedia = float(request.form.get('vMedia')) 
            valorA = int(request.form.get("valorA"))
            intervalo = request.form.get("intervalo")
            
            if request.form.get("valorB") and len(intervalo) > 18:
                valorB = int(request.form.get("valorB"))
            else: 
                valorB = 0
    return render_template("index.html", vMedia=vMedia, valorA=valorA, 
    valorB=valorB, intervalo=intervalo, mostrar_modal="poisson", dados_vac=True, dadosClasses={}, modaBruta=False, 
    FequenciaIndividualAbsolutaRecebida={}, FequenciaIndividualAbsoluta={}, FrequenciaAcumulada={}, TabelaDeDados={},
    Posicoes={}, escolhaCalculo=[], mostrarResultados=False)

@app.route("/regr_linear_eq_1", methods=["POST", "GET"])
def regr_linear_eq_1():
    resetar_variaveis()
    #Organiza os dados na tabela de FI
    if request.method == "POST":
        if request.form.get("valorX" and "valorY"):
            valorX = float(request.form.get('valorX'))
            valorY = float(request.form.get('valorY'))

            TabelaDeDados[valorX] = valorY
            print(TabelaDeDados)

        if request.form.get("limpar"):
            limparDados = request.form.get("limpar")
            TabelaDeDados.pop(float(limparDados))
    return render_template("index.html", mostrar_modal="equacao1",
    TabelaDeDados=TabelaDeDados, FequenciaIndividualAbsolutaRecebida={}, FequenciaIndividualAbsoluta={},
    FrequenciaAcumulada={}, Posicoes={}, dadosClasses=[], escolhaCalculo=[],mostrarResultados=False)


#Limpa os dados inseridos
@app.route("/limpar_dados", methods=["POST"])
def limpar_dados():
    global dadosDesordenados, FequenciaIndividualAbsolutaRecebida, FequenciaIndividualAbsoluta, dadosClasses, limiteSuperior, limiteInferior, vLambda, desvioPadrao, valorA, valorB, valorANorm, valorBNorm, tamanhoAmostraNorm, mediaNorm, desvioPadraoNorm, intervalo, reqDistNormal, secaoDNormalFinal, calcularNormal, moda, mediana, valorX, valorY, TabelaDeDados, probabSucesso, vTotal, vMedia
    dadosDesordenados = []; FequenciaIndividualAbsolutaRecebida = {}; FequenciaIndividualAbsoluta = {}; dadosClasses = []; TabelaDeDados = {}
    limiteSuperior = limiteInferior = vLambda = vMedia = desvioPadrao = 0
    valorA = valorB = valorANorm = valorBNorm = probabSucesso = vTotal = valorX = valorY  = 0
    tamanhoAmostraNorm = mediaNorm = desvioPadraoNorm = intervalo = 0
    reqDistNormal = secaoDNormalFinal = calcularNormal = False
    moda = mediana = None
    return render_template("index.html", FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={}, 
    FequenciaIndividualAbsolutaRecebida = {}, dadosClasses=[], TabelaDeDados={}, escolhaCalculo=[],mostrarResultados=False, mostrar_modal="padrao")

def resetar_variaveis():
    global dadosDesordenados, FequenciaIndividualAbsolutaRecebida, FequenciaIndividualAbsoluta, dadosClasses, limiteSuperior, limiteInferior, vLambda, desvioPadrao, valorA, valorB, valorANorm, valorBNorm, tamanhoAmostraNorm, mediaNorm, desvioPadraoNorm, intervalo, reqDistNormal, secaoDNormalFinal, calcularNormal, moda, mediana, valorX, valorY, TabelaDeDados, probabSucesso, vTotal, vMedia
    dadosDesordenados = []; FequenciaIndividualAbsolutaRecebida = {}; FequenciaIndividualAbsoluta = {}; dadosClasses = []; TabelaDeDados = {}
    limiteSuperior = limiteInferior = vLambda = vMedia = desvioPadrao = 0
    valorA = valorB = valorANorm = valorBNorm = probabSucesso = vTotal = valorX = valorY  = 0
    tamanhoAmostraNorm = mediaNorm = desvioPadraoNorm = intervalo = 0
    reqDistNormal = secaoDNormalFinal = calcularNormal = False
    moda = mediana = None

#Realiza as contas
@app.route("/calculo_dos_dados", methods=["POST"])
def calculo_dos_dados():
    global FequenciaIndividualAbsoluta, FequenciaIndividualAbsolutaRecebida, dadosClasses, limiteSuperior, limiteInferior, vLambda, desvioPadrao, valorA, valorB, valorCUnif, valorDUnif, valorANorm, valorBNorm, intervalo, desvioPadraoNorm, mediaNorm,tamanhoAmostraNorm, mostrar_modal, tipo, moda, mediana, vMedia
    
    erroOutroVazio = False
    tipo = request.form.get("tipo")
    if tipo == "outro":
        tipo = request.form.get("tipo_custom")
        if tipo.strip() == "":
            erroOutroVazio = True

    if erroOutroVazio:
        return render_template("index.html",
                               erroOutroVazio=True,
                               FequenciaIndividualAbsoluta={},
                               FrequenciaAcumulada={},
                               Posicoes={},
                               FequenciaIndividualAbsolutaRecebida={},
                               dadosClasses=[],
                               escolhaCalculo=[],
                               mostrarResultados=False)
    print("Tipo: ", tipo)
            
    escolhaCalculo = request.form.getlist("escolha-calculo")
    escolhaCalculoJson = json.dumps(escolhaCalculo).replace("'", '"')
        
    mostrar_modal = request.form.get("mostrar_modal", "")
    
    try:
        
        print("limiteSuperior", limiteSuperior)
        print("limiteInferior", limiteInferior)
        print("intervalo", intervalo)
        print("valorCUnif", valorCUnif)
        if limiteSuperior != 0 and limiteInferior != 0 and intervalo != "" and valorCUnif != "":
            return processar_dist_uniforme(limiteSuperior, limiteInferior, valorCUnif, valorDUnif, intervalo, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo)
        
        if vLambda != 0 or desvioPadrao != 0:
            if intervalo != "" and valorA != "":
                return processar_dist_exponencial(vLambda, desvioPadrao, valorA, valorB, intervalo, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo)

        if(valorANorm != "" and mediaNorm != 0 and desvioPadraoNorm != 0 and tamanhoAmostraNorm != None):
                return processar_dist_normal(valorANorm, valorBNorm, intervalo, mediaNorm, desvioPadraoNorm, tamanhoAmostraNorm, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo)

        if(vTotal != 0 and probabSucesso != 0 and intervalo != "" and valorA != ""):
            return processar_dist_binomial(vTotal, probabSucesso, valorA, valorB, intervalo, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo)

        if(vMedia != 0 and intervalo != "" and valorA != ""):
                return processar_dist_poisson(vMedia, valorA, valorB, intervalo, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo)

        if(TabelaDeDados):
                return processar_regr_linear_eq_1(TabelaDeDados, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo)

        # Mensagem de erro caso a pessoa não insira um valor para os cálculos 
        if not FequenciaIndividualAbsolutaRecebida and not dadosDesordenados and not dadosClasses:
            raise ValueError
        if len(dadosDesordenados) == 1:
            raise ValueError

        # Processamento para dados agrupados em classes
        if dadosClasses:
            if(request.form.get("btnCalcularDiscDistNormal")):
                mostrar_modal = "normal"
                return processar_dados_classes(dadosClasses, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo)
            else:
                return processar_dados_classes(dadosClasses, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo)

        #Organização dos dados inseridos em tabela
        elif FequenciaIndividualAbsolutaRecebida:
            FequenciaIndividualAbsoluta = dict(sorted(FequenciaIndividualAbsolutaRecebida.items()))
          
        #Cálculo do FI e organização da tabela se os dados inseridos forem os desordenados
        else:
            for dado in sorted(dadosDesordenados):
                if dado in FequenciaIndividualAbsoluta:
                    FequenciaIndividualAbsoluta[dado] += 1
                else:
                    FequenciaIndividualAbsoluta[dado] = 1
          
        #Tamanho da amostra
        tamanhoDaAmostra = f"{sum(FequenciaIndividualAbsoluta.values()):g}"
        
        #Frequência acumulada absoluta
        Fac = 0 
        FacAnt = 0
        FrequenciaAcumulada = {}
        Posicoes = {}
        for dado in sorted(FequenciaIndividualAbsoluta.keys()):
            Fac = FacAnt + FequenciaIndividualAbsoluta[dado]
            FacAjust = f"{Fac:g}"
            FrequenciaAcumulada[dado] = FacAjust
            
            #Calculo de posições 
            inicio = FacAnt + 1
            fim = Fac
            
            inicio = f"{inicio:g}"
            fim = f"{fim:g}" 
            if(inicio == fim):
                Posicoes[dado] = f"{fim}º"
            else:
                Posicoes[dado] = f"{inicio}º à {fim}º" 
            
            FacAnt = Fac       
        xifi = {}
        
        #Média
        for amostra, frequencia in sorted(FequenciaIndividualAbsoluta.items()):
            xifi[amostra] = amostra * frequencia
            
        media = round(sum(xifi.values())/sum(FequenciaIndividualAbsoluta.values()), 2)

        #Moda
        max_freq = max(FequenciaIndividualAbsoluta.values())
        moda = [valor for valor, freq in FequenciaIndividualAbsoluta.items() if freq == max_freq]
        if len(moda) == len(FequenciaIndividualAbsoluta):
            tipo_moda = 'Amodal'
        elif len(moda) == 1:
            tipo_moda = 'Unimodal'
        elif len(moda) == 2:
            tipo_moda = 'Bimodal'
        elif len(moda) == 3:
            tipo_moda = 'Trimodal'
        else:
            tipo_moda = 'Multimodal'

        #Mediana
        def calculo_mediana(dadosDesordenados, FequenciaIndividualAbsoluta):
            dados_mediana = []

            if dadosDesordenados:
                dados_mediana = sorted(dadosDesordenados)
            elif FequenciaIndividualAbsoluta:
                for valor, freq in FequenciaIndividualAbsoluta.items():
                    dados_mediana.extend([valor] * int(freq))
                dados_mediana.sort()
            else:
                return None, [] 
            
            n = len(dados_mediana)
            if n % 2 == 1:
                mediana = dados_mediana[n // 2]
            else:
                mediana = (dados_mediana[n // 2-1] + dados_mediana[n // 2]) / 2
            
            return mediana, dados_mediana

        mediana_calculada, dados_para_template = calculo_mediana(dadosDesordenados, FequenciaIndividualAbsoluta)

        if(len(dadosDesordenados) != 0 and len(dadosDesordenados) != 1):
            def calcular_variancia(valores):
                if len(valores) == 0:
                    return 0
                return sum((x - media) ** 2 for x in valores) / (len(valores) -1)  # populacional
            variancia = round(calcular_variancia(dadosDesordenados), 2)

            def calcular_desvio_padrao(valores):
                variancia = calcular_variancia(valores)
                return math.sqrt(variancia)
            desvioPadrao = round(calcular_desvio_padrao(dadosDesordenados), 2)

            def calcular_coeficiente_variacao(valores):
                desvio_padrao = round(calcular_desvio_padrao(valores),2)
                return (desvio_padrao * 100) / media  if media != 0 else float("inf")
            coeficienteVariacao = round(calcular_coeficiente_variacao(dadosDesordenados), 2)

        elif(len(FequenciaIndividualAbsoluta) != 0 and len(dadosDesordenados) != 1):
            # Criar lista expandida para cálculos de variância
            dados_expandidos = []
            for valor, freq in FequenciaIndividualAbsoluta.items():
                dados_expandidos.extend([valor] * int(freq))
            
            def calcular_variancia(valores):
                if len(valores) == 0:
                    return 0
                return sum((x - media) ** 2 for x in valores) / (len(valores) -1)
            variancia = round(calcular_variancia(dados_expandidos), 2)

            def calcular_desvio_padrao(valores):
                variancia = calcular_variancia(valores)
                return math.sqrt(variancia)
            desvioPadrao = round(calcular_desvio_padrao(dados_expandidos), 2)

            def calcular_coeficiente_variacao(valores):
                desvio_padrao = round(calcular_desvio_padrao(valores),2)
                print(desvio_padrao)
                print(media)
                return (desvio_padrao * 100) / media
            coeficienteVariacao = round(calcular_coeficiente_variacao(dados_expandidos), 2)
        else:
            variancia = 0
            desvioPadrao = 0
            coeficienteVariacao = 0
        
        print("reqDistNormal", reqDistNormal)
        if reqDistNormal:
            print("calcularNormal",calcularNormal)
            if(calcularNormal == True):
                return processar_dist_normal(valorANorm, valorBNorm, intervalo, mediaNorm, desvioPadraoNorm, tamanhoAmostraNorm, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo)

            else: 
                mediaNorm = media  # Atribui à variável global
                desvioPadraoNorm = desvioPadrao  # Atribui à variável global
                mediana = mediana_calculada  # Atribui à variável global
                tamanhoAmostraNorm = int(tamanhoDaAmostra)
                
                return render_template("index.html", 
                                    mediaNorm=media, 
                                    moda=moda, 
                                    tipo_moda=tipo_moda, 
                                    mediana=mediana, 
                                    variancia=variancia, 
                                    desvioPadraoNorm=desvioPadrao,
                                    tamanhoAmostraNorm=tamanhoAmostraNorm,
                                    coeficienteVariacao=coeficienteVariacao,
                                    escolhaCalculo=escolhaCalculo, 
                                    dadosDesordenados=dadosDesordenados, 
                                    FequenciaIndividualAbsoluta=FequenciaIndividualAbsoluta,
                                    tamanhoDaAmostra=tamanhoDaAmostra, 
                                    FrequenciaAcumulada=FrequenciaAcumulada, 
                                    Posicoes=Posicoes, 
                                    FequenciaIndividualAbsolutaRecebida={}, 
                                    dadosClasses=[], 
                                    TabelaDeDados={},
                                    mostrar_modal="normal",  # Mantém o modal aberto
                                    tipolhaCalculoJson=escolhaCalculoJson, 
                                    mostrarResultados=False,
                                    secaoDNormalFinal = True,
                                    # Adiciona flags para mostrar botão de prosseguir
                                    reqDistNormal=True)

            
        return render_template("index.html", media=media, moda=moda, tipo_moda=tipo_moda, mediana=mediana_calculada, variancia=variancia, desvioPadrao=desvioPadrao, 
        coeficienteVariacao=coeficienteVariacao,escolhaCalculo=escolhaCalculo, dadosDesordenados=dadosDesordenados, FequenciaIndividualAbsoluta=FequenciaIndividualAbsoluta,
        tamanhoDaAmostra=tamanhoDaAmostra, FrequenciaAcumulada=FrequenciaAcumulada, Posicoes=Posicoes, FequenciaIndividualAbsolutaRecebida={}, dadosClasses=[], 
        mostrar_modal=mostrar_modal, tipo=tipo, TabelaDeDados={}, escolhaCalculoJson=escolhaCalculoJson, mostrarResultados=True, erroOutroVazio=erroOutroVazio, erroDadosDesordenadosUmNum=erroDadosDesordenadosUmNum, dados_agrup_disc=True)
    except ValueError:
        return render_template("index.html", erro="Você precisa inserir pelo menos um dado!", FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, 
        Posicoes={}, FequenciaIndividualAbsolutaRecebida = {}, TabelaDeDados={}, dadosClasses=[], escolhaCalculo=[])

def processar_dados_classes(dadosClasses, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo):
    global reqDistNormal, desvioPadraoNorm, mediaNorm, tamanhoAmostraNorm, calcularNormal, valorANorm, valorBNorm, intervalo, moda, mediana
    """Processa dados agrupados em classes e calcula todas as estatísticas"""

    # Criar tabela para exibição
    tabela_classes = {}
    FrequenciaAcumulada = {}
    Posicoes = {}
    
    fac_anterior = 0
    for i, classe in enumerate(dadosClasses):
        intervaloClasses = f"[{classe['li']:.1f} - {classe['ls']:.1f})"
        fi = classe['fi']
        fac_atual = fac_anterior + fi
        
        tabela_classes[intervaloClasses] = fi
        FrequenciaAcumulada[intervaloClasses] = f"{fac_atual:g}"
        
        # Posições
        inicio = fac_anterior + 1
        fim = fac_atual
        if inicio == fim:
            Posicoes[intervaloClasses] = f"{int(fim)}º"
        else:
            Posicoes[intervaloClasses] = f"{int(inicio)}º à {int(fim)}º"
        
        fac_anterior = fac_atual
    
    # Tamanho da amostra
    tamanhoDaAmostra = sum(classe['fi'] for classe in dadosClasses)
    
    # Cálculos
    
    # 1. Média
    soma_xi_fi = sum(classe['xi'] * classe['fi'] for classe in dadosClasses)
    media = round(soma_xi_fi / tamanhoDaAmostra, 2)
    
    # 2. Moda de Czuber
    # Encontrar classe modal (maior frequência)
    classe_modal = max(dadosClasses, key=lambda x: x['fi'])
    
    # Frequências da classe anterior e posterior à modal
    idx_modal = next(i for i, c in enumerate(dadosClasses) if c == classe_modal)
    
    f_anterior = dadosClasses[idx_modal - 1]['fi'] if idx_modal > 0 else 0
    f_posterior = dadosClasses[idx_modal + 1]['fi'] if idx_modal < len(dadosClasses) - 1 else 0
    f_modal = classe_modal['fi']
    
    # Fórmula de Czuber
    h = classe_modal['ls'] - classe_modal['li']  # amplitude da classe
    delta1 = f_modal - f_anterior
    delta2 = f_modal - f_posterior
    
    if delta1 + delta2 != 0:
        modaCzuber = round(classe_modal['li'] + (delta1 / (delta1 + delta2)) * h, 2)
    else:
        modaCzuber = round(classe_modal['xi'], 2)  # usa ponto médio se denominador for zero
    
    # 3. Moda Bruta (classe com maior frequência)
    max_freq = max(classe['fi'] for classe in dadosClasses)
    modas_brutas = [classe['xi'] for classe in dadosClasses if classe['fi'] == max_freq]

    if len(modas_brutas) == len(dadosClasses):
        tipo_moda = 'Amodal'
        moda = "Não há moda"
    elif len(modas_brutas) == 1:
        tipo_moda = 'Unimodal'
        moda = f"{modas_brutas[0]}"
    elif len(modas_brutas) == 2:
        tipo_moda = 'Bimodal'
        moda = " e ".join(str(m) for m in modas_brutas)
    elif len(modas_brutas) == 3:
        tipo_moda = 'Trimodal'
        moda = " e ".join(str(m) for m in modas_brutas)
    else:
        tipo_moda = 'Multimodal'
        moda = ", ".join(str(m) for m in modas_brutas)
    
    # 4. Mediana
    posicao_mediana = tamanhoDaAmostra / 2
    fac_acumulado = 0
    classe_mediana = None
    fac_anterior_mediana = 0
    
    for classe in dadosClasses:
        fac_acumulado += classe['fi']
        if fac_acumulado >= posicao_mediana:
            classe_mediana = classe
            break
        fac_anterior_mediana = fac_acumulado
    
    if classe_mediana:
        h = classe_mediana['ls'] - classe_mediana['li']
        mediana = round(classe_mediana['li'] + ((posicao_mediana - fac_anterior_mediana) / classe_mediana['fi']) * h, 2)
    else:
        mediana = 0
    
    # 5. Variância (fórmula para dados agrupados)
    soma_xi_menos_media_ao_quadrado_fi = sum(((classe['xi'] - media) ** 2) * classe['fi'] for classe in dadosClasses)
    variancia = round(soma_xi_menos_media_ao_quadrado_fi / (tamanhoDaAmostra - 1), 2)

    # 6. DESVIO PADRÃO
    desvioPadrao = round(math.sqrt(variancia), 2)
    
    # 7. COEFICIENTE DE VARIAÇÃO
    coeficienteVariacao = round((desvioPadrao / media) * 100, 2) if media != 0 else float("inf")
    
    print("---------------------- Dados Classes ----------------------")
    print("reqDistNormal", reqDistNormal)
    if reqDistNormal:
        print("calcularNormal",calcularNormal)
        if(calcularNormal == True):
            return processar_dist_normal(valorANorm, valorBNorm, intervalo, mediaNorm, desvioPadraoNorm, tamanhoAmostraNorm, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo)
            
        else: 
            mediaNorm = media  # Atribui à variável 
            desvioPadraoNorm = desvioPadrao  # Atribui à variável global
            tamanhoAmostraNorm = int(tamanhoDaAmostra)
            
            return render_template("index.html", 
                                mediaNorm=media, 
                                moda=moda, 
                                modaCzuber=modaCzuber,
                                tipo_moda=tipo_moda, 
                                mediana=mediana,  
                                variancia=variancia, 
                                desvioPadraoNorm=desvioPadrao,
                                coeficienteVariacao=coeficienteVariacao,
                                escolhaCalculo=escolhaCalculo, 
                                dadosDesordenados=dadosDesordenados, 
                                FequenciaIndividualAbsoluta=FequenciaIndividualAbsoluta,
                                tamanhoDaAmostra=tamanhoDaAmostra, 
                                FrequenciaAcumulada=FrequenciaAcumulada, 
                                Posicoes=Posicoes, 
                                FequenciaIndividualAbsolutaRecebida={}, 
                                dadosClasses=[], 
                                TabelaDeDados={},
                                mostrar_modal="normal",  # Mantém o modal aberto
                                tipolhaCalculoJson=escolhaCalculoJson, 
                                mostrarResultados=False,
                                secaoDNormalFinal = True,
                                modaBruta=True,
                                # Adiciona flags para mostrar botão de prosseguir
                                reqDistNormal=True)
    
    
    return render_template("index.html", 
                         media=media, 
                         moda=moda, 
                         modaCzuber=modaCzuber,
                         tipo_moda=tipo_moda, 
                         modaBruta=True,
                         mediana=mediana, 
                         variancia=variancia, 
                         desvioPadrao=desvioPadrao,
                         coeficienteVariacao=coeficienteVariacao,
                         escolhaCalculo=escolhaCalculo, 
                         dadosDesordenados=[], 
                         TabelaDeDados={},
                         FequenciaIndividualAbsoluta=tabela_classes,
                         tamanhoDaAmostra=f"{tamanhoDaAmostra:g}",
                         FrequenciaAcumulada=FrequenciaAcumulada, 
                         Posicoes=Posicoes, 
                         FequenciaIndividualAbsolutaRecebida={}, 
                         dadosClasses=dadosClasses,
                         mostrar_modal="classes", 
                         tipo=tipo, 
                         escolhaCalculoJson=escolhaCalculoJson, 
                         mostrarResultados=True,
                         dados_classes=True) 

def processar_dist_uniforme(limiteSuperior, limiteInferior, valorCUnif, valorDUnif, intervalo, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo):
    print("---------------------------- processar_dist_uniforme ---------------------------- ")
    print("limiteSuperior", limiteSuperior)
    print("limiteInferior", limiteInferior)
    print("intervalo", intervalo)
    print("valorCUnif", valorCUnif)
    A = limiteInferior
    B = limiteSuperior
    distU = DistribuicaoUniforme(A, B)
        
    #1.paramentros
    media = round(distU.calcular_media(),2)
    variancia = round(distU.calcular_variancia(),2)
    desvioPadrao = round(distU.calcular_desvio_padrao(),2)
    coeficienteVariacao = round(distU.calcular_cv(),2)

    if(intervalo == "maiorQueUni" or intervalo == "maiorIgualUni"):
        resultProb = distU.calcular_probabilidade_intervalo(valorCUnif, B)
        print("prob_MaiorQue", resultProb)
    elif(intervalo == "menorQueUni" or intervalo == "menorIgualUni"):
        resultProb = distU.calcular_probabilidade_intervalo(A, valorCUnif)
        print("prob_MenorQue", resultProb)
    elif(intervalo == "intervaloIgualUni"):
        resultProb = 0.00
        print(resultProb)
    elif(len(intervalo) > 18):
        resultProb = distU.calcular_probabilidade_intervalo(valorCUnif, valorDUnif)
        print("menorQueMenorQue", resultProb)
    else:
        print("Tem algo errado")
    resultProb = round(resultProb,2)

    return render_template("index.html", 
                        limiteSuperior=limiteSuperior,
                        limiteInferior=limiteInferior,
                        valorCUnif=valorCUnif,
                        valorDUnif=valorDUnif,
                        intervalo=intervalo,
                         media=media, 
                         probabilidade=resultProb,
                         variancia=variancia, 
                         desvioPadrao=desvioPadrao,
                         coeficienteVariacao=coeficienteVariacao,
                         escolhaCalculo=escolhaCalculo, 
                         dadosDesordenados=[], 
                         FequenciaIndividualAbsoluta={},
                         FrequenciaAcumulada={}, 
                         Posicoes={}, 
                         TabelaDeDados={},
                         FequenciaIndividualAbsolutaRecebida={}, 
                         dadosClasses={},
                         tipo=tipo, 
                         escolhaCalculoJson=escolhaCalculoJson, 
                         mostrar_modal="uniforme",
                         mostrarResultados=True,
                         dados_vac=True) 

def processar_dist_exponencial(vLambda, desvioPadrao, valorA, valorB, intervalo, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo):
    if(vLambda != 0 and desvioPadrao == 0):
        exp_dist = DistribuicaoExponencial(taxa_lambda=vLambda)

        media = exp_dist.calcular_media()
        variancia = exp_dist.calcular_variancia()
        desvioPadrao = exp_dist.calcular_desvio_padrao()
        coeficienteVariacao = exp_dist.calcular_cv()

        if(valorA != "" and intervalo != ""):
            if(valorB != 0 and len(intervalo) > 18):
                resultProb = exp_dist.calcular_probabilidade_intervalo(valorA, valorB) 
                print(f"prob_intervalo {resultProb}")
            else: 
                if(intervalo == "maiorQueExpo" or intervalo == "maiorIgualExpo"):
                    resultProb = exp_dist.calcular_prob_sobrevivencia(valorA)
                    print("prob_MaiorQue ", resultProb)
                elif(intervalo == "menorQueExpo" or intervalo == "menorIgualExpo"):
                    resultProb = exp_dist.calcular_probabilidade_acumulada(valorA)
                    print("prob_MenorQue ", resultProb)
                elif(intervalo == "intervaloIgualExpo"):
                    resultProb = 0.00
                    print(resultProb)

    elif(desvioPadrao != 0 and vLambda == 0):
        vLambda = 1 / desvioPadrao
        exp_dist = DistribuicaoExponencial(taxa_lambda=vLambda)

        media = exp_dist.calcular_media()
        variancia = exp_dist.calcular_variancia()
        desvioPadrao = exp_dist.calcular_desvio_padrao()
        coeficienteVariacao = exp_dist.calcular_cv()
        
        media = round(media, 2)
        variancia = round(variancia, 2)
        desvioPadrao = round(desvioPadrao, 2)
        coeficienteVariacao = round(coeficienteVariacao, 2)

        print("Valor A: ", valorA)
        print("intervalo: ", intervalo)
        if(valorA != "" and intervalo != ""):
            if(valorB != 0 and len(intervalo) > 18):
                resultProb = exp_dist.calcular_probabilidade_intervalo(valorA, valorB) 
                print(f"prob_intervalo {resultProb}")
            else: 
                if(intervalo == "maiorQueExpo" or intervalo == "maiorIgualExpo"):
                    resultProb = exp_dist.calcular_prob_sobrevivencia(valorA)
                    print("prob_MaiorQue ", resultProb)
                elif(intervalo == "menorQueExpo" or intervalo == "menorIgualExpo"):
                    resultProb = exp_dist.calcular_probabilidade_acumulada(valorA)
                    print("prob_MenorQue ", resultProb)
                elif(intervalo == "intervaloIgualExpo"):
                    resultProb = 0.00
                    print(resultProb)
            resultProb = round(resultProb,2)
    else: 
        print("Tem algum erro ai")

    return render_template("index.html", 
                         media=media, 
                         probabilidade=resultProb,
                         valorA=valorA,
                         valorB=valorB,
                         variancia=variancia, 
                         desvioPadrao=desvioPadrao,
                         intervalo=intervalo,
                         coeficienteVariacao=coeficienteVariacao,
                         escolhaCalculo=escolhaCalculo, 
                         dadosDesordenados=[], 
                         FequenciaIndividualAbsoluta={},
                         TabelaDeDados={},
                         FrequenciaAcumulada={}, 
                         Posicoes={}, 
                         FequenciaIndividualAbsolutaRecebida={}, 
                         dadosClasses={},
                         mostrar_modal="exponencial", 
                         tipo=tipo, 
                         escolhaCalculoJson=escolhaCalculoJson, 
                         mostrarResultados=True,
                         dados_vac=True) 

def processar_dist_normal(valorANorm, valorBNorm, intervalo, mediaNorm, desvioPadraoNorm, tamanhoAmostraNorm, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo):
    global moda, mediana
    
    distN = DistribuicaoNormalPadrao()

    #1.paramentros
    media = distN.calcular_media()
    variancia = distN.calcular_variancia()
    desvioPadrao = distN.calcular_desvio_padrao()
    coeficienteVariacao = distN.calcular_cv()
    
    media = round(media,2)
    variancia = round(variancia,2)
    desvioPadrao = round(desvioPadrao,2)
    coeficienteVariacao = round(coeficienteVariacao,2)

    print('tamanhoAmostraNorm', tamanhoAmostraNorm)
    print('valorANorm', valorANorm)
    print('mediaNorm', mediaNorm)
    print('desvioPadraoNorm', desvioPadraoNorm)
    print('moda', moda)
    print('mediana', mediana)
    print('intervalo', intervalo)

    if(tamanhoAmostraNorm == 0 or tamanhoAmostraNorm == None):
        tamanhoAmostraNorm = None

    print('tamanhoAmostraNorm DEPOIS', tamanhoAmostraNorm)

    if(mediaNorm != 0 and desvioPadraoNorm != 0):
        valorANorm = TransformacaoZ.calcular_z_amostral(
        valorANorm, mediaNorm, desvioPadraoNorm, tamanhoAmostraNorm
    )
    if len(intervalo) > 20:
        valorBNorm = TransformacaoZ.calcular_z_amostral(
        valorBNorm, mediaNorm, desvioPadraoNorm, tamanhoAmostraNorm
    )

    if(intervalo == "maiorQueNormF" or intervalo == "maiorIgualNormF" or intervalo == "maiorQueNorm1" or intervalo == "maiorIgualNorm1"):
        resultProb = round(distN.calcular_prob_sobrevivencia(valorANorm) * 100, 2) 
        print("prob_MaiorQue", resultProb)
    elif(intervalo == "menorQueNormF" or intervalo == "menorIgualNormF" or intervalo == "menorQueNorm1" or intervalo == "menorIgualNorm1"):
        resultProb = round(distN.calcular_prob_acumulada(valorANorm) * 100, 2)
        print("prob_MenorQue", resultProb)
    elif(intervalo == "intervaloIgualNormF" or intervalo == "intervaloIgualNorm1"):
        resultProb = 0.00
        print(resultProb)
    elif(len(intervalo) > 20):
        resultProb = round(distN.calcular_probabilidade_intervalo(valorANorm, valorBNorm) * 100, 2) 
        print(valorANorm)
        print(valorBNorm)
        print("menorQueMenorQue", resultProb)
    else:
        print("Tem algo errado")

    return render_template("index.html", 
                         media=media, 
                         probabilidade=resultProb,
                         modaBruta=True,
                         mediana=mediana, 
                         moda=moda,
                         intervalo=intervalo,
                         desvioPadraoNorm=desvioPadraoNorm,
                         mediaNorm=mediaNorm,
                         tamanhoAmostraNorm=tamanhoAmostraNorm,
                         variancia=variancia, 
                         desvioPadrao=desvioPadrao,
                         coeficienteVariacao=coeficienteVariacao,
                         escolhaCalculo=escolhaCalculo, 
                         dadosDesordenados=[], 
                         FequenciaIndividualAbsoluta={},
                         FrequenciaAcumulada={}, 
                         Posicoes={}, 
                         FequenciaIndividualAbsolutaRecebida={}, 
                         dadosClasses={},
                         TabelaDeDados={},
                         mostrar_modal="normal",
                         tipo=tipo, 
                         escolhaCalculoJson=escolhaCalculoJson, 
                         mostrarResultados=True,
                         dados_vac=True,
                         reqDistNormal = True, 
                         calcularNormal = False) 

def processar_dist_binomial(vTotal, probabSucesso, valorA, valorB, intervalo, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo):
    print("------------- Binomial ---------------")
    print("vTotal", vTotal)
    print("probabSucesso", probabSucesso)
    print("valorA", valorA)
    print("valorB", valorB)
    print("intervalo", intervalo)
    if(vTotal != 0 and probabSucesso != 0):
        n = vTotal
        p = probabSucesso
        dist = DistribuicaoBinomial(n, p)

        media = dist.calcular_media()
        variancia = dist.calcular_variancia()
        desvio_padrao = dist.calcular_desvio_padrao()
        coeficienteVariacao = dist.calcular_cv()
        
        media = round(media,2)
        variancia = round(variancia,2)
        desvio_padrao = round(desvio_padrao,2)
        coeficienteVariacao = round(coeficienteVariacao,2)

        if(valorA != "" and intervalo != ""):
            if(valorB != 0 and intervalo in ["menorQueMenorQueBin", "menorIgualMenorQueBin", "menorQueMenorIgualBin", "menorIgualMenorIgualBin"]):
                match intervalo:
                    case "menorQueMenorQueBin":
                        resultProb = dist.calcular_probabilidade_intervalo(valorA + 1, valorB - 1)
                    case "menorIgualMenorQueBin":
                        resultProb = dist.calcular_probabilidade_intervalo(valorA, valorB - 1)
                    case "menorQueMenorIgualBin":
                        resultProb = dist.calcular_probabilidade_intervalo(valorA + 1, valorB)
                    case "menorIgualMenorIgualBin":
                        resultProb = dist.calcular_probabilidade_intervalo(valorA, valorB)
                resultProb = round(resultProb,2)
            elif(intervalo in ["maiorQueBin", "maiorIgualBin", "menorQueBin", "menorIgualBin", "intervaloIgualBin"]): 
                match intervalo:
                    case "maiorQueBin":
                        resultProb = 100 - dist.calcular_probabilidade_intervalo(0, valorA)
                    case "maiorIgualBin":
                        resultProb = 100 - dist.calcular_probabilidade_intervalo(0, valorA - 1)
                    case "menorQueBin":
                        resultProb = dist.calcular_probabilidade_intervalo(0, valorA - 1)
                    case "menorIgualBin":
                        resultProb = dist.calcular_probabilidade_intervalo(0, valorA)
                    case "intervaloIgualBin":
                        resultProb = dist.calcular_probabilidade(valorA) * 100
                resultProb = round(resultProb,2)
            else: 
                print("Tem algum erro ai")

    return render_template("index.html", 
                         media=media, 
                         probabilidade=resultProb,
                         variancia=variancia, 
                         desvioPadrao=desvio_padrao,
                         coeficienteVariacao=coeficienteVariacao,
                         escolhaCalculo=escolhaCalculo, 
                         vTotal=vTotal,
                         probabSucesso=probabSucesso,
                         valorA=valorA,
                         valorB=valorB,
                         intervalo=intervalo,
                         dadosDesordenados=[], 
                         FequenciaIndividualAbsoluta={},
                         FrequenciaAcumulada={}, 
                         Posicoes={}, 
                         FequenciaIndividualAbsolutaRecebida={}, 
                         dadosClasses={},
                         TabelaDeDados={},
                         mostrar_modal="binomial", 
                         tipo=tipo, 
                         escolhaCalculoJson=escolhaCalculoJson, 
                         mostrarResultados=True,
                        ) 

def processar_dist_poisson(vMedia, valorA, valorB, intervalo, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo):
    vLambda = vMedia
    print("------------- Poisson ---------------")
    print("vMedia", vMedia)
    print("valorA", valorA)
    print("valorB", valorB)
    print("intervalo", intervalo)
    print("vLambda", vLambda)
    if(vLambda != 0):
        dist = DistribuicaoPoisson(vLambda)

        media = dist.calcular_media()
        variancia = dist.calcular_variancia()
        desvio_padrao = dist.calcular_desvio_padrao()
        coeficienteVariacao = dist.calcular_coeficiente_variacao()
        
        media = round(media,2)
        variancia = round(variancia,2)
        desvio_padrao = round(desvio_padrao,2)
        coeficienteVariacao = round(coeficienteVariacao,2)

        if(valorA != "" and intervalo != ""):
            if(valorB != "" and intervalo in ["menorQueMenorQuePoi", "menorIgualMenorQuePoi", "menorQueMenorIgualPoi", "menorIgualMenorIgualPoi"]):
                match intervalo:
                    case "menorQueMenorQuePoi":
                        resultProb = dist.calcular_probabilidade_intervalo(valorA + 1, valorB - 1)
                    case "menorIgualMenorQuePoi":
                        resultProb = dist.calcular_probabilidade_intervalo(valorA, valorB - 1)
                    case "menorQueMenorIgualPoi":
                        resultProb = dist.calcular_probabilidade_intervalo(valorA + 1, valorB)
                    case "menorIgualMenorIgualPoi":
                        resultProb = dist.calcular_probabilidade_intervalo(valorA, valorB)
                resultProb = round(resultProb,2)
            elif(intervalo in ["maiorQuePoi", "maiorIgualPoi", "menorQuePoi", "menorIgualPoi", "intervaloIgualPoi"]): 
                match intervalo:
                    case "maiorQuePoi":
                        resultProb = 100 - dist.calcular_probabilidade_intervalo(0, valorA)
                    case "maiorIgualPoi":
                        resultProb = 100 - dist.calcular_probabilidade_intervalo(0, valorA - 1)
                    case "menorQuePoi":
                        resultProb = dist.calcular_probabilidade_intervalo(0, valorA - 1)
                    case "menorIgualPoi":
                        resultProb = dist.calcular_probabilidade_intervalo(0, valorA)
                    case "intervaloIgualPoi":
                        resultProb = dist.calcular_probabilidade(valorA) * 100
                resultProb = round(resultProb,2)
            else: 
                print("Tem algum erro ai")

    return render_template("index.html", 
                         media=media, 
                         probabilidade=resultProb,
                         variancia=variancia, 
                         desvioPadrao=desvio_padrao,
                         coeficienteVariacao=coeficienteVariacao,
                         escolhaCalculo=escolhaCalculo, 
                         intervalo=intervalo,
                         vMedia=vMedia,
                         valorA=valorA,
                         valorB=valorB,
                         dadosDesordenados=[], 
                         FequenciaIndividualAbsoluta={},
                         FrequenciaAcumulada={}, 
                         Posicoes={}, 
                         FequenciaIndividualAbsolutaRecebida={}, 
                         dadosClasses={},
                         TabelaDeDados={},
                         mostrar_modal="poisson", 
                         tipo=tipo, 
                         escolhaCalculoJson=escolhaCalculoJson, 
                         mostrarResultados=True,
                        ) 

def processar_regr_linear_eq_1(TabelaDeDados, escolhaCalculo, escolhaCalculoJson, mostrar_modal, tipo):
    print("------------- Equação 1º Grau ---------------")
    print("TabelaDeDados", TabelaDeDados)
    if(TabelaDeDados != 0):
        reg = RegressaoLinear(TabelaDeDados)

        equacaoReta = reg.equacao_reta()
        coefiDeterminacao = reg.calcular_coeficiente_determinacao()
        dominio = reg.calcular_dominio()
        
        coefiDeterminacao = round(coefiDeterminacao, 2)
        
        print("equacaoReta", equacaoReta)
        print("coefiDeterminacao", coefiDeterminacao)
        print("dominio", dominio)

    else: 
        print("Tem algum erro ai")

    return render_template("index.html", 
                         equacaoReta=equacaoReta, 
                         coefiDeterminacao=coefiDeterminacao,
                         escolhaCalculo=escolhaCalculo, 
                         dominio=dominio,
                         dadosDesordenados=[], 
                         FequenciaIndividualAbsoluta={},
                         FrequenciaAcumulada={}, 
                         Posicoes={}, 
                         TabelaDeDados={},
                         FequenciaIndividualAbsolutaRecebida={}, 
                         dadosClasses={},
                         mostrar_modal="equacao1", 
                         tipo=tipo, 
                         escolhaCalculoJson=escolhaCalculoJson, 
                         mostrarResultados=True,
                        ) 


#distribuicao uniforme
class DistribuicaoUniforme:
    def __init__(self, A: float, B: float):
        if A >= B:
            raise ValueError('O limite inferior (A) deve ser menor que o limite superior (B).')
        self.A = A
        self.B = B
        self.amplitude = B - A

    def calcular_media(self) -> float:
        media = (self.A + self.B) / 2
        return media
    
    def calcular_variancia(self) -> float:
        variancia = (self.amplitude ** 2) / 12
        return variancia
    
    def calcular_desvio_padrao(self) -> float:
        desvio_padrao = math.sqrt(self.calcular_variancia())
        return desvio_padrao
    
    def calcular_cv(self) -> float:
        desvio_padrao = self.calcular_desvio_padrao()
        media = self.calcular_media()
        if media == 0:
            return float('inf')
        cv = (desvio_padrao / media) * 100
        return cv
    
    def calcular_probabilidade_intervalo(self, x1:float, x2:float) -> float:
        #calcula P(x1 <= X <= x2)
        if x1 > x2:
            x1, x2 = x2,x1
        limite_inferior = max(x1, self.A)
        limite_superior = min(x2, self.B)

        if limite_inferior >= limite_superior:
                return 0.0
            
        probabilidade = (limite_superior - limite_inferior) / self.amplitude
        return probabilidade * 100

    #retorna o valor da função densidade de probilidade f(x) para um dado ponto x
    def densidade_probabilidade(self, x: float) -> float:
        if self.A <= x <= self.B:
            return 1 / self.amplitude
        else:
            return 0.0

#distribuicao exponencial
class DistribuicaoExponencial:

    def __init__(self, taxa_lambda: float ):
        if taxa_lambda <= 0:
            raise ValueError('O parâmetro lambda deve ser positivo')
        self.taxa_lambda = taxa_lambda

    def calcular_media(self) -> float:
        return 1 / self.taxa_lambda
    
    def calcular_variancia(self) -> float:
        return 1 / (self.taxa_lambda ** 2)
    
    def calcular_desvio_padrao(self) -> float:
        return self.calcular_media()
    
    def calcular_cv(self) -> float:
        return 100.0
    
    def calcular_probabilidade_acumulada(self, A: float) -> float:
        #calcula a probabilidade P(X <= A)
        if A < 0:
            return 0.0
        prob = 100 * (1 - math.exp(-self.taxa_lambda * A))
        return prob
    
    def calcular_prob_sobrevivencia(self, A: float) -> float:
        #calcula a probabilidade P(X >= A)
        if A < 0:
            return 100.0
        prob = 100 * math.exp(-self.taxa_lambda * A)
        return prob
    
    def calcular_probabilidade_intervalo(self, x1: float, x2: float) -> float:
        #calcula a probabilidade P(x1 <= X <= x2)
        if x1 > x2:
            x1, x2 = x2, x1
        prob_x2 = self.calcular_probabilidade_acumulada(x2)
        prob_x1 = self.calcular_probabilidade_acumulada(x1)
        return prob_x2 - prob_x1
        
#-- Distribuição Normal Padronizada --
class DistribuicaoNormalPadrao:
    def __init__(self):
        self.media = 0
        self.desvio_padrao = 1.0
        self.variancia = 1.0

    def calcular_media(self) -> float:
        return self.media
    
    def calcular_variancia(self) -> float:
        return self.variancia
    
    def calcular_desvio_padrao(self) -> float:
        return self.desvio_padrao
    
    def calcular_cv(self) -> float:
        return float('inf')
    
    def calcular_prob_acumulada(self, z: float) -> float:
        #P(Z <= a)
        prob = norm.cdf(z)
        return prob
    
    def calcular_prob_sobrevivencia(self, z: float) -> float:
        #P(Z >= a)
        prob = norm.sf(z)
        return prob
    
    def calcular_probabilidade_intervalo(self, z1: float, z2: float) -> float:
        if z1 > z2:
            z1, z2 = z2, z1
        prob_z2 = self.calcular_prob_acumulada(z2)
        prob_z1 = self.calcular_prob_acumulada(z1)
        return prob_z2 - prob_z1
    
#conversor x pra z
class TransformacaoZ:
    @staticmethod
    def calcular_z_amostral(X: float, media: float, desvio_amostral: float, n: int) -> float:
        if desvio_amostral <= 0:
            raise ValueError("Desvio-padrão deve ser positivo.")

        erro_padrao = desvio_amostral / math.sqrt(n)   # fórmula amostral: s / √n
        Z = (X - media) / erro_padrao
        return Z

#-- Distribuição Binomial --    
class DistribuicaoBinomial:
    def __init__(self, n: int, p: float):
        if n <= 0:
            raise ValueError("O número de tentativas (n) deve ser positivo.")
        if not (0 <= p <= 1):
            raise ValueError("A probabilidade (p) deve estar entre 0 e 1.")
        self.n = n
        self.p = p
        self.q = 1 - p

    def calcular_media(self):
        return self.n * self.p

    def calcular_variancia(self):
        return self.n * self.p * self.q

    def calcular_desvio_padrao(self):
        return math.sqrt(self.calcular_variancia())

    def calcular_cv(self):
        media = self.calcular_media()
        desvio_padrao = self.calcular_desvio_padrao()
        if media == 0:
            return float('inf')
        return (desvio_padrao / media) * 100

    def calcular_probabilidade(self, k: int):
        """P(X = k)"""
        if k < 0 or k > self.n:
            return 0.0
        comb = (math.comb(self.n, k))
        prob = comb * (self.p ** k) * (self.q ** (self.n - k))
        return prob

    def calcular_probabilidade_intervalo(self, k1: int, k2: int):
        """P(k1 <= X <= k2)"""
        if k1 > k2:
            k1, k2 = k2, k1
        prob = sum(self.calcular_probabilidade(k) for k in range(k1, k2 + 1))
        return prob * 100

#-- Distribuição Poisson --
class DistribuicaoPoisson:
    def __init__(self, vLambda: float):
        if vLambda <= 0:
            raise ValueError('Lambda deve ser positivo.')
        self.vLambda = vLambda

    def calcular_media(self):
        return self.vLambda

    def calcular_variancia(self):
        return self.vLambda

    def calcular_desvio_padrao(self):
        return math.sqrt(self.vLambda)

    def calcular_coeficiente_variacao(self):
        media = self.calcular_media()
        desvio_padrao = self.calcular_desvio_padrao()
        if (media == 0):
          return float('inf')
        return (desvio_padrao / media) * 100

    def calcular_probabilidade(self, x: int):
        """P(X = x)"""
        if x < 0:
            return 0
        prob = (math.exp(-self.vLambda) * (self.vLambda ** x)) / math.factorial(x)
        return prob

    def calcular_probabilidade_intervalo(self, x1: int, x2: int):
        """P(x1 <= X <= x2)"""
        if x1 > x2:
            x1, x2 = x2, x1
        prob = sum(self.calcular_probabilidade(x) for x in range(x1, x2 + 1))
        return prob * 100

#-- Regressão Linear - Equação 1º Grau --
class RegressaoLinear:
    def __init__(self, dados: dict[float, float]):
        if not dados:
            raise ValueError("O dicionário de dados não pode estar vazio.")
        
        self.x = list(dados.keys())
        self.y = list(dados.values())
        self.n = len(self.x)

        self.soma_x = sum(self.x)
        self.soma_y = sum(self.y)
        self.soma_x2 = sum([xi**2 for xi in self.x])
        self.soma_y2 = sum([yi**2 for yi in self.y])
        self.soma_xy = sum([self.x[i] * self.y[i] for i in range(self.n)])

    def calcular_coeficiente_angular(self):
        numerador = (self.n * self.soma_xy) - (self.soma_x * self.soma_y)
        denominador = (self.n * self.soma_x2) - (self.soma_x ** 2)
        if denominador == 0:
            raise ValueError("Divisão por zero no cálculo do coeficiente angular.")
        return numerador / denominador

    def calcular_coeficiente_linear(self):
        b = self.calcular_coeficiente_angular()
        a = (self.soma_y - b * self.soma_x) / self.n
        return a 

    def calcular_coeficiente_correlacao(self):
        numerador = (self.n * self.soma_xy) - (self.soma_x * self.soma_y)
        denominador = math.sqrt(
            (self.n * self.soma_x2 - self.soma_x**2) *
            (self.n * self.soma_y2 - self.soma_y**2)
        )
        if denominador == 0:
            raise ValueError("Divisão por zero no cálculo do coeficiente de correlação.")
        return numerador / denominador

    def calcular_coeficiente_determinacao(self):
        r = self.calcular_coeficiente_correlacao()
        return (r**2) * 100

    def prever(self, x_novo: float):
        a = self.calcular_coeficiente_linear()
        b = self.calcular_coeficiente_angular()
        y_previsto = a + b * x_novo
        return y_previsto

    def equacao_reta(self):
        a = self.calcular_coeficiente_linear()
        b = self.calcular_coeficiente_angular()
        return f"y = {round(a,2)} + {round(b,2)}x"
    
    def calcular_dominio(self):
        x_min = min(self.x)
        x_max = max(self.x)
        return (x_min, x_max)


if __name__ == '__main__':
    app.run(debug=True)