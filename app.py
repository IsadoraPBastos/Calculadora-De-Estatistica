# pip install flask
import json
import math
from flask import Flask, render_template, request

app = Flask(__name__)

dadosDesordenados = []
FequenciaIndividualAbsolutaRecebida = {}
FequenciaIndividualAbsoluta = {}
dadosClasses = []  

@app.route('/')
def index():
    return render_template('index.html', FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={}, 
                           FequenciaIndividualAbsolutaRecebida = {}, dadosClasses=[], escolhaCalculo=[],mostrarResultados=False)

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
    FequenciaIndividualAbsolutaRecebida = {}, dadosClasses=[], escolhaCalculo=[],mostrarResultados=False)

#Recebe os dados quando a pessoa envia eles pela parte de tabela
@app.route("/dados_em_tabela", methods=["POST", "GET"])
def dados_em_tabela():
    #Organiza os dados na tabela de FI
    if request.method == "POST":
        if request.form.get("amostra" and "frequencia"):
            amostra = float(request.form.get('amostra'))
            frequencia = float(request.form.get('frequencia'))

            FequenciaIndividualAbsolutaRecebida[amostra] = frequencia
            
            dadosDesordenados.clear()
            dadosClasses.clear()
        elif request.form.get("limpar"):
            amostraLimpar = request.form.get("limpar")
            FequenciaIndividualAbsolutaRecebida.pop(float(amostraLimpar))
    return render_template("index.html", mostrar_modal="discreto", mostrar_desor_ou_tab="tabela", 
    FequenciaIndividualAbsolutaRecebida=FequenciaIndividualAbsolutaRecebida, FequenciaIndividualAbsoluta={},
    FrequenciaAcumulada={}, Posicoes={}, dadosClasses=[], escolhaCalculo=[],mostrarResultados=False)

@app.route("/agrupamento_classes", methods=["POST", "GET"])
def agrupamento_classes():
    global dadosClasses
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
    escolhaCalculo=[], mostrarResultados=False)

@app.route("/alteração_fi", methods=["POST", "GET"])
def alteração_fi():
    global dadosClasses
    if request.method == "POST":
        for i, classe in enumerate(dadosClasses):
            fi = request.form.get(f'fi_{i}')
            if fi:
                classe['fi'] = int(fi)

        if request.form.get("limpar") == "limpar":
            dadosClasses.clear()
            

    return render_template("index.html", mostrar_modal="classes", 
    dadosClasses=dadosClasses, modaBruta=True, FequenciaIndividualAbsolutaRecebida={}, 
    FequenciaIndividualAbsoluta={}, FrequenciaAcumulada={}, Posicoes={}, 
    escolhaCalculo=[], mostrarResultados=False)

#Limpa os dados inseridos
@app.route("/limpar_dados", methods=["POST"])
def limpar_dados():
    global dadosDesordenados, FequenciaIndividualAbsoluta, FequenciaIndividualAbsolutaRecebida, dadosClasses
    dadosDesordenados = []
    FequenciaIndividualAbsoluta = {}
    FequenciaIndividualAbsolutaRecebida = {}
    dadosClasses = []
    return render_template("index.html", FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={}, 
    FequenciaIndividualAbsolutaRecebida = {}, dadosClasses=[], escolhaCalculo=[],mostrarResultados=False)

#Realiza as contas
@app.route("/calculo_dos_dados", methods=["POST"])
def calculo_dos_dados():
    global FequenciaIndividualAbsoluta, FequenciaIndividualAbsolutaRecebida, dadosClasses
    
    erroOutroVazio = False
    tipo = request.form.get("tipo")
    if tipo == "outro":
        tipo = request.form.get("tipo_custom")
        print(tipo)
        if tipo == "":
            erroOutroVazio = True
            
    escolhaCalculo = request.form.getlist("escolha-calculo")
    escolhaCalculoJson = json.dumps(escolhaCalculo).replace("'", '"')
        
    modal_aberto = request.form.get("modal_aberto", "")
    
    try:
        #Mensagem de erro caso a pessoa não insira um valor para os cálculos 
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
                return sum((x - media) ** 2 for x in valores) / len(valores)  # populacional
            variancia = round(calcular_variancia(dadosDesordenados), 2)

            def calcular_desvio_padrao(valores):
                variancia = calcular_variancia(valores)
                return math.sqrt(variancia)
            desvioPadrao = round(calcular_desvio_padrao(dadosDesordenados), 2)

            def calcular_coeficiente_variacao(valores):
                desvio_padrao = calcular_desvio_padrao(valores)
                return (desvio_padrao / media) * 100 if media != 0 else float("inf")
            coeficienteVariacao = round(calcular_coeficiente_variacao(dadosDesordenados), 2)

        elif(len(FequenciaIndividualAbsoluta) != 0):
            # Criar lista expandida para cálculos de variância
            dados_expandidos = []
            for valor, freq in FequenciaIndividualAbsoluta.items():
                dados_expandidos.extend([valor] * int(freq))
            
            def calcular_variancia(valores):
                if len(valores) == 0:
                    return 0
                return sum((x - media) ** 2 for x in valores) / len(valores)
            variancia = round(calcular_variancia(dados_expandidos), 2)

            def calcular_desvio_padrao(valores):
                variancia = calcular_variancia(valores)
                return math.sqrt(variancia)
            desvioPadrao = round(calcular_desvio_padrao(dados_expandidos), 2)

            def calcular_coeficiente_variacao(valores):
                desvio_padrao = calcular_desvio_padrao(valores)
                return (desvio_padrao / media) * 100 if media != 0 else float("inf")
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
                         dados_classes=True)  # Flag para indicar que são dados de classes

if __name__ == '__main__':
    app.run(debug=True)