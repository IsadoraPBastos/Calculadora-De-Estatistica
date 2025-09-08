# pip install flask
import json
from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)

dadosDesordenados = []

@app.route('/')
def index():
    return render_template('index.html', FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={}, 
                           FequenciaIndividualAbsolutaRecebida = {}, escolhaCalculo=[])

#Recebe os dados quando a pessoa envia eles pela parte desordenada 
@app.route("/dados_desordenados", methods=["POST", "GET"])
def dados_desordenados():
    if request.method == "POST":
        if request.form.get("dado"):
            dadosDesordenados.append(float(request.form.get("dado")))
    return render_template("index.html", mostrar_modal="desordenado", dadosDesordenados=dadosDesordenados, 
    FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={}, FequenciaIndividualAbsolutaRecebida = {}, escolhaCalculo=[])


FequenciaIndividualAbsolutaRecebida = {}
#Recebe os dados quando a pessoa envia eles pela parte de tabela
@app.route("/dados_em_tabela", methods=["POST", "GET"])
def dados_em_tabela():
    #Organiza os dados na tabela de FI
    if request.method == "POST":
        if request.form.get("amostra" and "frequencia"):
            amostra = float(request.form.get('amostra'))
            frequencia = float(request.form.get('frequencia'))

            FequenciaIndividualAbsolutaRecebida[amostra] = frequencia
            
    return render_template("index.html", mostrar_modal="tabela", 
    FequenciaIndividualAbsolutaRecebida=FequenciaIndividualAbsolutaRecebida, FequenciaIndividualAbsoluta={},
    FrequenciaAcumulada={}, Posicoes={}, escolhaCalculo=[])

#Limpa os dados inseridos
@app.route("/limpar_dados", methods=["POST"])
def limpar_dados():
    global dadosDesordenados
    dadosDesordenados = []
    global FequenciaIndividualAbsoluta
    FequenciaIndividualAbsoluta = {}
    global FequenciaIndividualAbsolutaRecebida
    FequenciaIndividualAbsolutaRecebida = {}
    return render_template("index.html", FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={}, 
    FequenciaIndividualAbsolutaRecebida = {}, escolhaCalculo=[])

FequenciaIndividualAbsoluta = {}

#Realiza as contas
@app.route("/calculo_dos_dados", methods=["POST"])
def calculo_dos_dados():
    global FequenciaIndividualAbsoluta
    global FequenciaIndividualAbsolutaRecebida
    
    
    tipo = request.form.get("tipo")
    if tipo == "outro":
        tipo = request.form.get("tipo_custom")
            
    escolhaCalculo = request.form.getlist("escolha-calculo")
    escolhaCalculoJson = json.dumps(escolhaCalculo)
        
    modal_aberto = request.form.get("modal_aberto", "")
    try:
        #Mensagem de erro caso a pessoa não insira um valor para os cálculos 
        if not FequenciaIndividualAbsolutaRecebida and not dadosDesordenados:
            raise ValueError
        
        #Organização dos dados inseridos em tabela
        elif FequenciaIndividualAbsolutaRecebida:
            FequenciaIndividualAbsoluta = dict(sorted(FequenciaIndividualAbsolutaRecebida.items()))
            
        #Cálculo do FI e organização da tabela se os dados inseridos forem os desordenados
        else :
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
        #provavelmente vai ter que criar algum tipo de salvamento pras listas originais, funções como .sort e .extend modificam as listas originais
        #a váriavel de frequência individual absoluta está escrita como 'Fequencia'
            
        return render_template("index.html", media=media, moda=moda, tipo_moda=tipo_moda, mediana=mediana_calculada, 
        escolhaCalculo=escolhaCalculo, dadosDesordenados=dadosDesordenados, FequenciaIndividualAbsoluta=FequenciaIndividualAbsoluta,
        tamanhoDaAmostra=tamanhoDaAmostra, FrequenciaAcumulada=FrequenciaAcumulada, Posicoes=Posicoes, 
        FequenciaIndividualAbsolutaRecebida={}, mostrar_modal=modal_aberto, tipo=tipo, escolhaCalculoJson=escolhaCalculoJson)
    except ValueError:
        return render_template("index.html", erro="Você precisa inserir pelo menos um dado!", FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, 
        Posicoes={}, FequenciaIndividualAbsolutaRecebida = {}, escolhaCalculo=[])
        
#import math

# Lista de dados recebida
#FequenciaIndividualAbsolutaRecebida = [10, 20, 30, 40]

def calcular_media(valores):
    if len(valores) == 0:
        return 0
    return sum(valores) / len(valores)
    
def calcular_variancia(valores):
    if len(valores) == 0:
        return 0
    media = calcular_media(valores)
    return sum((x - media) ** 2 for x in valores) / len(valores)  # populacional

def calcular_desvio_padrao(valores):
    variancia = calcular_variancia(valores)
    return math.sqrt(variancia)

def calcular_coeficiente_variacao(valores):
    media = calcular_media(valores)
    desvio_padrao = calcular_desvio_padrao(valores)
    return (desvio_padrao / media) * 100 if media != 0 else float("inf")

#def calcular_estatisticas(valores):
   # return {
     #   "Média": round(calcular_media(valores), 2),
      #  "Variância": round(calcular_variancia(valores), 2),
      #  "Desvio Padrão": round(calcular_desvio_padrao(valores), 2),
      #  "Coeficiente de Variação (%)": round(calcular_coeficiente_variacao(valores), 2)
   # }

# Exemplo de uso
#resultado = calcular_estatisticas(FequenciaIndividualAbsolutaRecebida)
#for chave, valor in resultado.items():
   # print(f"{chave}: {valor}")
    

if __name__ == '__main__':

    app.run(debug=True)


