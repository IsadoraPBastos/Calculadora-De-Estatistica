from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)

dadosDesordenados = []

@app.route('/')
def index():
    return render_template('index.html', FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={})

#Recebe os dados quando a pessoa envia eles pela parte desordenada 
@app.route("/dados_desordenados", methods=["POST", "GET"])
def dados_desordenados():
    if request.method == "POST":
        if request.form.get("dado"):
            dadosDesordenados.append(float(request.form.get("dado")))
    return render_template("index.html", dadosDesordenados=dadosDesordenados, FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={}, FequenciaIndividualAbsolutaRecebida = {})


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
            
    return render_template("index.html", FequenciaIndividualAbsolutaRecebida = FequenciaIndividualAbsolutaRecebida, FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={})

#Limpa os dados inseridos
@app.route("/limpar_dados", methods=["POST"])
def limpar_dados():
    global dadosDesordenados
    dadosDesordenados = []
    global FequenciaIndividualAbsoluta
    FequenciaIndividualAbsoluta = {}
    global FequenciaIndividualAbsolutaRecebida
    FequenciaIndividualAbsolutaRecebida = {}
    return render_template("index.html", FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={}, FequenciaIndividualAbsolutaRecebida = {})

FequenciaIndividualAbsoluta = {}

#Realiza as contas
@app.route("/calculo_dos_dados", methods=["POST"])
def calculo_dos_dados():
    global FequenciaIndividualAbsoluta
    global FequenciaIndividualAbsolutaRecebida
    if FequenciaIndividualAbsolutaRecebida:
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
        Posicoes[dado] = f"{inicio}º à {fim}º" 
        
        FacAnt = Fac       
    xifi = {}
    
    #Média
    for amostra, frequencia in sorted(FequenciaIndividualAbsoluta.items()):
        xifi[amostra] = amostra * frequencia
        
    media = round(sum(xifi.values())/sum(FequenciaIndividualAbsoluta.values()), 2)
          
    return render_template("index.html", media=media, dadosDesordenados=dadosDesordenados, FequenciaIndividualAbsoluta=FequenciaIndividualAbsoluta, tamanhoDaAmostra=tamanhoDaAmostra, FrequenciaAcumulada=FrequenciaAcumulada, Posicoes=Posicoes, FequenciaIndividualAbsolutaRecebida = {})

if __name__ == '__main__':
    app.run(debug=True)