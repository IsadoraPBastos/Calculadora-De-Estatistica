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
    return render_template("index.html", dadosDesordenados=dadosDesordenados, FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={})

FequenciaIndividualAbsoluta = {}

#Recebe os dados quando a pessoa envia eles pela parte de tabela
@app.route("/dados_em_tabela", methods=["POST", "GET"])
def dados_em_tabela():
    #Organiza os dados na tabela de FI
    if request.method == "POST":
        if request.form.get("amostra" and "frequencia"):
            amostra = float(request.form.get('amostra'))
            frequencia = float(request.form.get('frequencia'))

            FequenciaIndividualAbsoluta[amostra] = frequencia
            
    return render_template("index.html", FequenciaIndividualAbsoluta=FequenciaIndividualAbsoluta,FrequenciaAcumulada={}, Posicoes={})

#Limpa os dados inseridos
@app.route("/limpar_dados", methods=["POST"])
def limpar_dados():
    global dadosDesordenados
    dadosDesordenados = []
    global FequenciaIndividualAbsoluta
    FequenciaIndividualAbsoluta = {}
    return render_template("index.html", FequenciaIndividualAbsoluta={},FrequenciaAcumulada={}, Posicoes={})

#Realiza as contas
@app.route("/calculo_dos_dados", methods=["POST"])
def calculo_dos_dados():
    #Cálculo do FI e organização da tabela se os dados inseridos forem os desordenados
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
        FrequenciaAcumulada[dado] = Fac
        
        #Calculo de posições 
        inicio = FacAnt + 1
        fim = Fac
        Posicoes[dado] = f"{inicio}º à {fim}º" 
        
        FacAnt = Fac       
    
        
    return render_template("index.html", dadosDesordenados=dadosDesordenados, FequenciaIndividualAbsoluta=FequenciaIndividualAbsoluta, tamanhoDaAmostra=tamanhoDaAmostra, FrequenciaAcumulada=FrequenciaAcumulada, Posicoes=Posicoes)

if __name__ == '__main__':
    app.run(debug=True)