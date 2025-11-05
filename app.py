# pip install flask
import json
import math
from flask import Flask, render_template, request, Response
import math
from scipy.stats import norm #pip install scipy

app = Flask(__name__)

dadosDesordenados = []
FequenciaIndividualAbsolutaRecebida = {}
FequenciaIndividualAbsoluta = {}
dadosClasses = []  
num1 = 0
num2 = 0
vLambda = 0
desvioPadrao = 0

@app.route('/')
def index():
    return render_template('index.html', FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={}, 
    FequenciaIndividualAbsolutaRecebida = {}, dadosClasses=[], escolhaCalculo=[], num1=0, num2=0, vLambda=0, mostrarResultados=False)

#Recebe os dados quando a pessoa envia eles pela parte desordenada 
@app.route("/dados_desordenados", methods=["POST", "GET"])
def dados_desordenados():
    if request.method == "POST":
        if request.form.get("dado"):
            dadosDesordenados.append(float(request.form.get("dado")))
            FequenciaIndividualAbsolutaRecebida.clear()
            FequenciaIndividualAbsoluta.clear()
            dadosClasses.clear()
        elif request.form.get("limpar") == "limpar":
            dadosDesordenados.clear()
    return render_template("index.html", mostrar_modal="discreto", mostrar_desor_ou_tab="desordenado", 
    dadosDesordenados=dadosDesordenados, FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={}, 
    FequenciaIndividualAbsolutaRecebida = {}, dadosClasses=[], escolhaCalculo=[],mostrarResultados=False, num1=0, num2=0)

#Recebe os dados quando a pessoa envia eles pela parte de tabela
@app.route("/dados_em_tabela", methods=["POST", "GET"])
def dados_em_tabela():
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
    return render_template("index.html", mostrar_modal="discreto", mostrar_desor_ou_tab="tabela", 
    FequenciaIndividualAbsolutaRecebida=FequenciaIndividualAbsolutaRecebida, FequenciaIndividualAbsoluta={},
    FrequenciaAcumulada={}, Posicoes={}, dadosClasses=[], escolhaCalculo=[],mostrarResultados=False, erroFIMenorZero=erroFIMenorZero, 
    num1=0, num2=0)

@app.route("/agrupamento_classes", methods=["POST", "GET"])
def agrupamento_classes():
    global dadosClasses
    dadosClasses.clear()
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
            
    return render_template("index.html", mostrar_modal="classes", 
    dadosClasses=dadosClasses, modaBruta=True, FequenciaIndividualAbsolutaRecebida={}, 
    FequenciaIndividualAbsoluta={}, FrequenciaAcumulada={}, Posicoes={}, 
    escolhaCalculo=[], mostrarResultados=False, num1=0, num2=0)

@app.route("/alteração_fi", methods=["POST", "GET"])
def alteração_fi():
    global dadosClasses
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
    escolhaCalculo=[], mostrarResultados=False, erroMenorZero=erroMenorZero, num1=0, num2=0)

@app.route("/dist_uniforme", methods=["POST", "GET"])
def dist_uniforme():
    global num1, num2
    if request.method == "POST":
        if request.form.get("num1") and request.form.get("num2"):
            num1 = float(request.form.get('num1'))
            num2 = float(request.form.get('num2'))           
            

    return render_template("index.html", num1=num1, num2=num2, mostrar_modal="uniforme", 
    dadosClasses={}, modaBruta=True, FequenciaIndividualAbsolutaRecebida={}, 
    FequenciaIndividualAbsoluta={}, FrequenciaAcumulada={}, Posicoes={}, 
    escolhaCalculo=[], mostrarResultados=False)

@app.route("/dist_exponencial", methods=["POST", "GET"])
def dist_exponencial():
    global vLambda, desvioPadrao, valorA, valorB, intervalo
    if request.method == "POST":
        if request.form.get("vLambda") and request.form.get("valorA") and request.form.get("intervalo"):
            if request.form.get("valorB"):
                vLambda = float(request.form.get('vLambda')) 
                valorA = float(request.form.get("valorA"))
                valorB = float(request.form.get("valorB"))
                intervalo = request.form.get("intervalo")
                desvioPadrao = 0
            else: 
                vLambda = float(request.form.get('vLambda')) 
                valorA = float(request.form.get("valorA"))
                intervalo = request.form.get("intervalo")
                desvioPadrao = 0
                valorB = 0
        elif request.form.get("desvioPadrao") and request.form.get("valorA") and request.form.get("intervalo"):
            if request.form.get("valorB"):
                valorA = float(request.form.get("valorA"))
                valorB = float(request.form.get("valorB"))
                intervalo = request.form.get("intervalo")
                desvioPadrao = float(request.form.get("desvioPadrao"))
                vLambda = 0
            else: 
                valorA = float(request.form.get("valorA"))
                intervalo = request.form.get("intervalo")
                desvioPadrao = float(request.form.get("desvioPadrao"))
                vLambda = 0
                valorB = 0

    return render_template("index.html", vLambda=vLambda, desvioPadrao=desvioPadrao, valorA=valorA, 
    valorB=valorB, intervalo=intervalo, mostrar_modal="exponencial", dadosClasses={}, modaBruta=True, 
    FequenciaIndividualAbsolutaRecebida={}, FequenciaIndividualAbsoluta={}, FrequenciaAcumulada={}, 
    Posicoes={}, escolhaCalculo=[], mostrarResultados=False)

#Limpa os dados inseridos
@app.route("/limpar_dados", methods=["POST"])
def limpar_dados():
    global dadosDesordenados, FequenciaIndividualAbsoluta, FequenciaIndividualAbsolutaRecebida, dadosClasses, num1, num2, vLambda
    dadosDesordenados = []
    FequenciaIndividualAbsoluta = {}
    FequenciaIndividualAbsolutaRecebida = {}
    dadosClasses = []
    num1=0
    num2=0
    vLambda=0
    desvioPadrao=0
    return render_template("index.html", FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={}, 
    FequenciaIndividualAbsolutaRecebida = {}, dadosClasses=[], escolhaCalculo=[],mostrarResultados=False)

#Realiza as contas
@app.route("/calculo_dos_dados", methods=["POST"])
def calculo_dos_dados():
    global FequenciaIndividualAbsoluta, FequenciaIndividualAbsolutaRecebida, dadosClasses, num1, num2, vLambda, desvioPadrao, valorA, valorB, intervalo
    
    erroOutroVazio = False
    tipo = request.form.get("tipo")
    if tipo == "outro":
        tipo = request.form.get("tipo_custom")
        print(tipo)
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
            
    escolhaCalculo = request.form.getlist("escolha-calculo")
    escolhaCalculoJson = json.dumps(escolhaCalculo).replace("'", '"')
        
    modal_aberto = request.form.get("modal_aberto", "")
    
    try:
        #Mensagem de erro caso a pessoa não insira um valor para os cálculos 
        if num1 != 0 and num2 != 0:
            return processar_dist_uniforme(num1, num2, escolhaCalculo, escolhaCalculoJson, modal_aberto, tipo)
        
        if vLambda != 0 or desvioPadrao != 0:
            if intervalo != "" and valorA != 0:
                return processar_dist_exponencial(vLambda, desvioPadrao, valorA, valorB, intervalo, escolhaCalculo, escolhaCalculoJson, modal_aberto, tipo)

        if not FequenciaIndividualAbsolutaRecebida and not dadosDesordenados and not dadosClasses:
            raise ValueError
        
        # Processamento para dados agrupados em classes
        if dadosClasses:
            return processar_dados_classes(dadosClasses, escolhaCalculo, escolhaCalculoJson, modal_aberto, tipo)

        
            
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

        if(len(dadosDesordenados) != 0):
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

        elif(len(FequenciaIndividualAbsoluta) != 0):
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
            
        return render_template("index.html", media=media, moda=moda, tipo_moda=tipo_moda, mediana=mediana_calculada, variancia=variancia, desvioPadrao=desvioPadrao, 
        coeficienteVariacao=coeficienteVariacao,escolhaCalculo=escolhaCalculo, dadosDesordenados=dadosDesordenados, FequenciaIndividualAbsoluta=FequenciaIndividualAbsoluta,
        tamanhoDaAmostra=tamanhoDaAmostra, FrequenciaAcumulada=FrequenciaAcumulada, Posicoes=Posicoes, FequenciaIndividualAbsolutaRecebida={}, dadosClasses=[], 
        mostrar_modal=modal_aberto, tipo=tipo, escolhaCalculoJson=escolhaCalculoJson, mostrarResultados=True, erroOutroVazio=erroOutroVazio)
    except ValueError:
        return render_template("index.html", erro="Você precisa inserir pelo menos um dado!", FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, 
        Posicoes={}, FequenciaIndividualAbsolutaRecebida = {}, dadosClasses=[], escolhaCalculo=[])

def processar_dados_classes(dadosClasses, escolhaCalculo, escolhaCalculoJson, modal_aberto, tipo):
    """Processa dados agrupados em classes e calcula todas as estatísticas"""

    # Criar tabela para exibição
    tabela_classes = {}
    FrequenciaAcumulada = {}
    Posicoes = {}
    
    fac_anterior = 0
    for i, classe in enumerate(dadosClasses):
        intervalo = f"[{classe['li']:.1f} - {classe['ls']:.1f})"
        fi = classe['fi']
        fac_atual = fac_anterior + fi
        
        tabela_classes[intervalo] = fi
        FrequenciaAcumulada[intervalo] = f"{fac_atual:g}"
        
        # Posições
        inicio = fac_anterior + 1
        fim = fac_atual
        if inicio == fim:
            Posicoes[intervalo] = f"{int(fim)}º"
        else:
            Posicoes[intervalo] = f"{int(inicio)}º à {int(fim)}º"
        
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
                         FequenciaIndividualAbsoluta=tabela_classes,
                         tamanhoDaAmostra=f"{tamanhoDaAmostra:g}",
                         FrequenciaAcumulada=FrequenciaAcumulada, 
                         Posicoes=Posicoes, 
                         FequenciaIndividualAbsolutaRecebida={}, 
                         dadosClasses=dadosClasses,
                         mostrar_modal=modal_aberto, 
                         tipo=tipo, 
                         escolhaCalculoJson=escolhaCalculoJson, 
                         mostrarResultados=True,
                         dados_classes=True) 

def processar_dist_uniforme(num1, num2, escolhaCalculo, escolhaCalculoJson, modal_aberto, tipo):
    distU = DistribuicaoUniforme(A=num1, B=num2)

    #1.paramentros
    media = distU.calcular_media()
    variancia = distU.calcular_variancia()
    desvioPadrao = distU.calcular_desvio_padrao()
    coeficienteVariacao = distU.calcular_cv()

    return render_template("index.html", 
                         media=media, 
                        #  moda=moda, 
                        #  modaCzuber=modaCzuber,
                        #  tipo_moda=tipo_moda, 
                         modaBruta=True,
                        #  mediana=mediana, 
                         variancia=variancia, 
                         desvioPadrao=desvioPadrao,
                         coeficienteVariacao=coeficienteVariacao,
                         escolhaCalculo=escolhaCalculo, 
                         dadosDesordenados=[], 
                         FequenciaIndividualAbsoluta={},
                         #tamanhoDaAmostra=f"{tamanhoDaAmostra:g}",
                         FrequenciaAcumulada={}, 
                         Posicoes={}, 
                         FequenciaIndividualAbsolutaRecebida={}, 
                         dadosClasses={},
                         mostrar_modal=modal_aberto, 
                         tipo=tipo, 
                         escolhaCalculoJson=escolhaCalculoJson, 
                         mostrarResultados=True) 

def processar_dist_exponencial(vLambda, desvioPadrao, valorA, valorB, intervalo, escolhaCalculo, escolhaCalculoJson, modal_aberto, tipo):
    if(vLambda != 0 and desvioPadrao == 0):
        exp_dist = DistribuicaoExponencial(taxa_lambda=vLambda)

        media = exp_dist.calcular_media()
        variancia = exp_dist.calcular_variancia()
        desvioPadrao = exp_dist.calcular_desvio_padrao()
        coeficienteVariacao = exp_dist.calcular_cv()

        if(valorA != 0 and intervalo != ""):
            if(valorB != 0 and intervalo == "menorQueMenorQue"):
                prob_intervalo = exp_dist.calcular_probabilidade_intervalo(valorA, valorB) 
                print("prob_intervalo " + prob_intervalo)
            else: 
                if(intervalo == "maiorQue"):
                    prob_MaiorQue = exp_dist.calcular_prob_sobrevivencia(valorA)
                    print("prob_MaiorQue ", prob_MaiorQue)
                elif(intervalo == "menorQue"):
                    prob_MenorQue = exp_dist.calcular_probabilidade_acumulada(valorA)
                    print("prob_MenorQue ", prob_MenorQue)

    elif(desvioPadrao != 0 and vLambda == 0):
        vLambda = 1 / desvioPadrao
        exp_dist = DistribuicaoExponencial(taxa_lambda=vLambda)

        media = exp_dist.calcular_media()
        variancia = exp_dist.calcular_variancia()
        desvioPadrao = exp_dist.calcular_desvio_padrao()
        coeficienteVariacao = exp_dist.calcular_cv()

        print("Valor A: ", valorA)
        print("intervalo: ", intervalo)
        if(valorA != 0 and intervalo != ""):
            if(valorB != 0 and intervalo == "menorQueMenorQue"):
                prob_intervalo = exp_dist.calcular_probabilidade_intervalo(valorA, valorB) 
                print("prob_intervalo " + prob_intervalo)
            else: 
                if(intervalo == "maiorQue"):
                    prob_MaiorQue = exp_dist.calcular_prob_sobrevivencia(valorA)
                    print("prob_MaiorQue ", prob_MaiorQue)
                elif(intervalo == "menorQue"):
                    prob_MenorQue = exp_dist.calcular_probabilidade_acumulada(valorA)
                    print("prob_MenorQue ", prob_MenorQue)
    else: 
        print("Tem algum erro ai")

    return render_template("index.html", 
                         media=media, 
                        #  moda=moda, 
                        #  modaCzuber=modaCzuber,
                        #  tipo_moda=tipo_moda, 
                         modaBruta=True,
                        #  mediana=mediana, 
                         variancia=variancia, 
                         desvioPadrao=desvioPadrao,
                         coeficienteVariacao=coeficienteVariacao,
                         escolhaCalculo=escolhaCalculo, 
                         dadosDesordenados=[], 
                         FequenciaIndividualAbsoluta={},
                         #tamanhoDaAmostra=f"{tamanhoDaAmostra:g}",
                         FrequenciaAcumulada={}, 
                         Posicoes={}, 
                         FequenciaIndividualAbsolutaRecebida={}, 
                         dadosClasses={},
                         mostrar_modal=modal_aberto, 
                         tipo=tipo, 
                         escolhaCalculoJson=escolhaCalculoJson, 
                         mostrarResultados=True) 


#distribuicao uniforme
class DistribuicaoUniforme:
    def __init__(self, A: float, B: float):
        if A >= B:
            raise ValueError('O limite inferior (A) deve ser menor que o limite superior (B).')
        self.A = A
        self.B = B
        self.amplitude = B - A

    def calcular_media(self) -> float:
        media = round((self.A + self.B) / 2, 2)
        return media
    
    def calcular_variancia(self) -> float:
        variancia = round((self.amplitude ** 2) / 12, 2)
        return variancia
    
    def calcular_desvio_padrao(self) -> float:
        desvio_padrao = round(math.sqrt(self.calcular_variancia()))
        return desvio_padrao
    
    def calcular_cv(self) -> float:
        desvio_padrao = self.calcular_desvio_padrao()
        media = self.calcular_media()
        if media == 0:
            return float('inf')
        cv = round((desvio_padrao / media) * 100, 2)
        return cv
    
    def calcular_probabilidade_intervalo(self, x1:float, x2:float) -> float:
        #calcula P(x1 <= X <= x2)
        if x1 > x2:
            x1, x2 = x2,x1
        limite_inferior = max(x1, self.A)
        limite_superior = min(x2, self.B)

        if limite_inferior >= limite_superior:
                return 0.0
            
        probabilidade = round((limite_superior - limite_inferior) / self.amplitude,2)
        return probabilidade * 100

    #retorna o valor da função densidade de probilidade f(x) para um dado ponto x
    def densidade_probabilidade(self, x: float) -> float:
        if self.A <= x <= self.B:
            return 1 / self.amplitude
        else:
            return 0.0

#--- EXERCICIO PASSADO PELO JC ---
A = -2.75 #-27,5 ou -2.75?
B = 10.17 
print(f'\nDistribuição Uniforme Contínua em A={A} e B={B}\n')
try:
    dist = DistribuicaoUniforme(A=A, B=B)

    #1.paramentros
    media = dist.calcular_media()
    variancia = dist.calcular_variancia()
    desvio_padrao = dist.calcular_desvio_padrao()
    cv = dist.calcular_cv()

    print(f'Intervalo[A, B]: [{dist.A}. {dist.B}]\n')
    print(f'A) Média: {media:.2f}\n')
    print(f'B) Variância: {variancia:.2f}\n')
    print(f'C) Desvio Padrão: {desvio_padrao:.2f}\n')
    print(f'D) Coeficiente de Variação (CV): {cv:.2f}%\n')

    #2.probabilidades
    prob_e = dist.calcular_probabilidade_intervalo(3, 6.98)
    print(f'E) P(3 < X < 6.98): {prob_e:.2f}%\n')

    prob_f = dist.calcular_probabilidade_intervalo(7.77, B)
    print(f'F) P(X >= 7.77): {prob_f:.2f}%\n')

    prob_g = dist.calcular_probabilidade_intervalo(A, 5.00)
    print(f'G) P(X < 5.00): {prob_g:.2f}%\n')

    prob_h = dist.calcular_probabilidade_intervalo(4.57, 4.57)
    print(f'H) P(X = 4.57): {prob_h:.2f}%\n')

except ValueError as e:
    print(f'Erro: {e}')

#distribuicao exponencial
class DistribuicaoExponencial:

    def __init__(self, taxa_lambda: float ):
        if taxa_lambda <= 0:
            raise ValueError('O parâmetro lambda deve ser positivo')
        self.taxa_lambda = taxa_lambda

    def calcular_media(self) -> float:
        return round(1 / self.taxa_lambda, 2)
    
    def calcular_variancia(self) -> float:
        return round(1 / (self.taxa_lambda ** 2),2)
    
    def calcular_desvio_padrao(self) -> float:
        return round(self.calcular_media(),2)
    
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
        

# --- EXERCICIO PASSADO PELO JC ---
DESVIO_PADRAO = 5.47

LAMBDA = 1 / DESVIO_PADRAO

print(f'\nDistribuição Exponencial')
print(f'Desvio Padrão dado: {DESVIO_PADRAO:.2f}')
print(f'Taxa calculada: {LAMBDA:.2f}')
try:
    exp_dist = DistribuicaoExponencial(taxa_lambda=LAMBDA)
    
    media = exp_dist.calcular_media()
    print(f'Média de conferência: {media:.2f}\n')

    prob_a = exp_dist.calcular_prob_sobrevivencia(6.99)
    print(f'A) P(X > 6.99): {prob_a:.2f}%\n')

    prob_b = exp_dist.calcular_probabilidade_acumulada(3.33)
    print(f'B) P(X <= 3.33): {prob_b:.2F}%\n')

    prob_c = exp_dist.calcular_probabilidade_intervalo(17, 17)
    print(f'C) P(X = 17): {prob_c:.2F}%\n')

    prob_d = exp_dist.calcular_probabilidade_intervalo(4, 5.50)
    print(f'D) P(4 < X <= 5,50): {prob_d:.2f}%\n')  
except ValueError as e:
    print(f'Erro: {e}')

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
        #P(Z <= a) = P(Z < a)
        prob = norm.cdf(z)
        return prob * 100
    
    def calcular_prob_sobrevivencia(self, z: float) -> float:
        #P(Z >= a) = P(Z > a)
        prob = norm.sf(z)
        return prob * 100
    
    def calcular_probabilidade_intervalo(self, z1: float, z2: float) -> float:
        #P(a <= Z <= b) = P(a < Z < b)
        if z1 > z2:
            z1, z2 = z2, z1
        prob_z2 = self.calcular_prob_acumulada(z2)
        prob_z1 = self.calcular_prob_acumulada(z1)

        return prob_z2 - prob_z1

#conversor x pra z
class TransformacaoZ:
    def calcular_z_tabela_amostra(X: float, Mu: float, Sigma: float, N: int) -> float:
        if N <= 0:
            raise ValueError('O tamanho da amostra (N) deve ser positivo')
        if Sigma <= 0:
            raise ValueError('O Desvio Padrão (Sigma) deve ser positivo')
        
        numerador = X - Mu
        raiz_N = math.sqrt(N)
        Z_tabela = (numerador * raiz_N) / Sigma
        return Z_tabela
    
# --- EXERCICIO DE EXEMPLO ---
MEDIA_POPULACIONAL = 25.42  
TAMANHO_AMOSTRA = 36        
DESVIO_POPULACIONAL = 7.25  
MEDIA_AMOSTRAL_INTERESSE = 23.99

print("\n\n--- Distribuição Amostral ---")
print(f'Dados: média ={MEDIA_POPULACIONAL}, amostra ={TAMANHO_AMOSTRA}, D.P ={DESVIO_POPULACIONAL} para P(X > 23.99)\n')

try:
    z_calculado = TransformacaoZ.calcular_z_tabela_amostra(
        X=MEDIA_AMOSTRAL_INTERESSE, 
        Mu=MEDIA_POPULACIONAL, 
        Sigma=DESVIO_POPULACIONAL, 
        N=TAMANHO_AMOSTRA
    )

    print(f'1. Tabela Z (Z_x) calculado: {z_calculado:.4f}')
    
    z_dist = DistribuicaoNormalPadrao()
    
    prob_a = z_dist.calcular_prob_sobrevivencia(z_calculado)
    
    print(f'2. Probabilidade P(Z > {z_calculado:.4f}): {prob_a:.2f}%')

    # A) P(X > 23.99)
    print(f'\nA) P(X > 23.99): {prob_a:.2f}%')

except ValueError as e:
    print(f'Erro: {e}')
except NameError:
    print("Erro: Certifique que as classes 'TransformacaoZ' e 'DistribuicaoNormalPadrao' estão definidas.")

    
if __name__ == '__main__':
    app.run(debug=True)