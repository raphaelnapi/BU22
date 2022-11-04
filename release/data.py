import os
import asn1
import json

import network as Net
import bu as BU
import log as Log

Estados = {
}

def salvaAmostra(texto, filename):
    file = open("Amostras\\{0}.txt".format(filename), "wt")
    file.write(texto)
    file.close()

def getCodeMunicipio(UF, municipio):
    ret = "none"
    for mun in Estados[UF.upper()]:
        if mun["nm"].lower() == municipio.lower():
            ret = mun["cd"]
    return ret

def criaPastaData():
    if not os.path.isdir("data"):
        os.mkdir("data")

def criaPastaUF(UF):
    criaPastaData()

    if not os.path.isdir("data\{0}".format(UF)):
        os.mkdir("data\{0}".format(UF))

def criaPastaMunicipio(UF, municipio):
    criaPastaUF(UF)

    if not os.path.isdir("data\\{0}\\{1}".format(UF, municipio)):
        os.mkdir("data\\{0}\\{1}".format(UF, municipio))

def appendToCSV(data, filename="analise.csv"):
    file = open(filename, "at")
    file.write("\n{0}".format(data))
    file.close()

#cria arquivo CSV com dados de todos os BU
def criaArquivoCSV(UF, filename="analise.csv"):
    filename = "data\\CSV\\" + filename

    #titulo
    cabecalho_bu = "UF; Municipio; Cod Municipio; Zona; Local; Secao; Data Hora Carga; Codigo Carga; N/S FC; N/S FV; Numero Interno Urna; Versao Votacao; Tipo Urna; Eleitores Aptos; Eleitores Comparecimento; Comparecimento com Biometria; Faltosos; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; Hora Abertura; Hora Encerramento; Hora Emissão"
    cabecalho_log = "Habilitacao Biometrica; Sem Biometria; Biometria FALHOU; Eleitores que Votaram; Tentativa de Votos; Titulo Invalido; Mesario Indagado se Eleitor Votando; Eleitor Ja Votou; Media Intervalo entre Eleitores; Maior Intervalo"
    appendToCSV(cabecalho_bu + "; " + cabecalho_log, filename)

    Municipios = Net.getMunicipios(UF)
    for Municipio in Municipios:
        Zonas = Net.getZonas(UF, Municipio)
        for Zona in Zonas:
            Secoes = Net.getSecoes(UF, Municipio, Zona)

            for Secao in Secoes:
                bu = BU.objBU(UF, Municipio, Zona, Secao)
                log = Log.objLog(UF, Municipio, Zona, Secao)
                appendToCSV(bu.toCSV() + "; " + log.toCSV(), filename)
                print("Municipio: {0} Zona {1} Secao {2} concluida.".format(Municipio, Zona, Secao))