import os
import asn1
import json

import network as Net
import bu as BU
import log as Log
import const

Estados = {
}

def getMunicipios(UF):
    ret = []
    for municipio in Estados[UF.upper()]:
        ret.append(municipio["nm"])

    return ret

def getZonas(UF, municipio):
    cdmun = getCodeMunicipio(UF, municipio)

    for mun in Estados[UF.upper()]:
        if mun["cd"] == cdmun:
            return mun["z"]

def getSecoes(UF, Municipio, Zona):
    file = open("{0}\\Secoes\\Secoes_{1}_{2}_{3}.dat".format(const.datapath, UF, Municipio, Zona), "rt")
    content = file.read()
    file.close()
    return content.split(";")

def salvaArquivo(conteudo, filename):
    file = open(filename, "wt")
    file.write(conteudo)
    file.close()

def loadMunicipiosJSON():
    file = open("{0}\\MunicipiosJSON.dat".format(const.datapath))
    content = file.read()
    file.close()

    municipios = json.loads(content)
    ret = {
    }

    for municipio in municipios["abr"]:
        ret[municipio["cd"]] = json.loads(json.dumps(municipio["mu"]))

    return ret

def salvaAmostra(texto, filename):
    file = open("Amostras\\{0}.txt".format(filename), "wt")
    file.write(texto)
    file.close()

def getCodeMunicipio(UF, municipio):
    for mun in Estados[UF.upper()]:
        if mun["nm"].lower() == municipio.lower():
            return mun["cd"]

def getMunicipioByCode(UF, cod_mun):
    for mun in Estados[UF.upper()]:
        if mun["cd"] == cod_mun:
            return mun["nm"]

def criaPastaData():
    if not os.path.isdir(const.datapath):
        os.mkdir(const.datapath)

def criaPastaUrnas():
    if not os.path.isdir(const.urnaspath):
        os.mkdir(const.urnaspath)

def criaPastaTurno(downloaddir_root=const.urnaspath):
    criaPastaUrnas()

    if not os.path.isdir(downloaddir_root):
        os.mkdir(downloaddir_root)

def criaPastaUF(UF, downloaddir_root=const.urnaspath):
    criaPastaTurno(downloaddir_root)

    if not os.path.isdir("{0}\\{1}".format(downloaddir_root, UF)):
        os.mkdir("{0}\\{1}".format(downloaddir_root, UF))

def criaPastaMunicipio(UF, municipio, downloaddir_root=const.urnaspath):
    criaPastaUF(UF, downloaddir_root)

    if not os.path.isdir("{0}\\{1}\\{2}".format(downloaddir_root, UF, municipio)):
        os.mkdir("{0}\\{1}\\{2}".format(downloaddir_root, UF, municipio))

def appendToCSV(data, filename="analise.csv"):
    file = open(filename, "at")
    file.write("\n{0}".format(data))
    file.close()

#cria arquivo CSV com dados de todos os BU
def criaArquivosCSV(UF, Turno):

    match Turno:
        case 1:
            cod_turno = const.TURNO.Primeiro
            pasta_turno = "Turno1"
        case 2:
            cod_turno = const.TURNO.Segundo
            pasta_turno = "Turno2"

    csv_dir = "{0}\\CSV\\{1}\\{2}".format(const.datapath, pasta_turno, UF)

    if not os.path.exists("{0}\\CSV\\{1}".format(const.datapath, pasta_turno)):
        os.mkdir("{0}\\CSV\\{1}".format(const.datapath, pasta_turno))

    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)

    #Configuração de cabeçalho do arquivo CSV
    cabecalho_bu = "UF;Municipio;Cod Municipio;Zona;Local;Secao;Data Hora Carga; Codigo Carga;N/S FC;N/S FV;Numero Interno Urna;Versao Votacao;Tipo Urna;Eleitores Aptos;Comparecimento;Votos Validos;Soma Votos Validos;Comparecimento com Biometria;Faltosos;Partido;Qtd Voto;Partido;Qtd Voto;Percentual sobre Votos Validos;Soma Votos;Percentual sobre Total;Partido;Qtd Voto;Partido;Qtd Voto;Partido;Qtd Voto;Partido;Qtd Voto;Partido;Qtd Voto;Percentual Votos Validos;Soma Votos;Soma Percentual;Partido;Qtd Voto;Partido;Qtd Voto;Partido;Qtd Voto;Partido;Qtd Voto;Branco;Qtd;Nulo;Qtd;Hora Abertura;Hora Encerramento;Hora Emissão"
    cabecalho_log = "Habilitacao Biometrica;Sem Biometria;Biometria FALHOU;Eleitores que Votaram;Tentativa de Votos;Titulo Invalido;Mesario Indagado se Eleitor Votando;Eleitor Ja Votou;Media Intervalo entre Eleitores;Maior Intervalo;Modelo Urna;UE2009;UE2010;UE2011;UE2013;UE2015;UE2020;OUTRO MODELO"

    #Cria Arquivo
    #Todos os dados
    stdfilepath = "{0}\\{1}.csv".format(csv_dir, UF)
    file = open(stdfilepath, "w")
    file.write(cabecalho_bu + ";" + cabecalho_log)
    file.close()

    #UE2009
    ue2009filepath = "{0}\\{1} UE2009.csv".format(csv_dir, UF)
    file = open(ue2009filepath, "w")
    file.write(cabecalho_bu + ";" + cabecalho_log)
    file.close()

    #UE2010
    ue2010filepath = "{0}\\{1} UE2010.csv".format(csv_dir, UF)
    file = open(ue2010filepath, "w")
    file.write(cabecalho_bu + ";" + cabecalho_log)
    file.close()

    #UE2011
    ue2011filepath = "{0}\\{1} UE2011.csv".format(csv_dir, UF)
    file = open(ue2011filepath, "w")
    file.write(cabecalho_bu + ";" + cabecalho_log)
    file.close()

    #UE2013
    ue2013filepath = "{0}\\{1} UE2013.csv".format(csv_dir, UF)
    file = open(ue2013filepath, "w")
    file.write(cabecalho_bu + ";" + cabecalho_log)
    file.close()

    #UE2015
    ue2015filepath = "{0}\\{1} UE2015.csv".format(csv_dir, UF)
    file = open(ue2015filepath, "w")
    file.write(cabecalho_bu + ";" + cabecalho_log)
    file.close()

    #UE2020
    ue2020filepath = "{0}\\{1} UE2020.csv".format(csv_dir, UF)
    file = open(ue2020filepath, "w")
    file.write(cabecalho_bu + ";" + cabecalho_log)
    file.close()

    CSVLine_std = 2
    CSVLine_UE2009 = 2
    CSVLine_UE2010 = 2
    CSVLine_UE2011 = 2
    CSVLine_UE2013 = 2
    CSVLine_UE2015 = 2
    CSVLine_UE2020 = 2

    Municipios = getMunicipios(UF)
    for Municipio in Municipios:
        Zonas = getZonas(UF, Municipio)
        for Zona in Zonas:
            Secoes = getSecoes(UF, Municipio, Zona)

            for Secao in Secoes:
                try:
                    #Carrega dados de BU e Log
                    bu = BU.objBU(UF, Municipio, Zona, Secao, Turno)
                    log = Log.objLog(UF, Municipio, Zona, Secao, Turno)

                    #Registra dados no arquivo geral    
                    lineToAppend = bu.toCSV(CSVLine_std) + ";" + log.toCSV()

                    #Registra dados no arquivo do Modelo de Urna
                    csv_line_modeloUrna = 2
                    filepath_modeloUrna = ""

                    modeloUrna = log.getModeloUrna()

                    match modeloUrna:
                        case "UE2009":
                            csv_line_modeloUrna = CSVLine_UE2009
                            filepath_modeloUrna = ue2009filepath
                        case "UE2010":
                            csv_line_modeloUrna = CSVLine_UE2010
                            filepath_modeloUrna = ue2010filepath
                        case "UE2011":
                            csv_line_modeloUrna = CSVLine_UE2011
                            filepath_modeloUrna = ue2011filepath
                        case "UE2013":
                            csv_line_modeloUrna = CSVLine_UE2013
                            filepath_modeloUrna = ue2013filepath
                        case "UE2015":
                            csv_line_modeloUrna = CSVLine_UE2015
                            filepath_modeloUrna = ue2015filepath
                        case "UE2020":
                            csv_line_modeloUrna = CSVLine_UE2020
                            filepath_modeloUrna = ue2020filepath

                    try:
                        lineToAppend = bu.toCSV(csv_line_modeloUrna) + ";" + log.toCSV()
                    except:
                        lineToAppend = "{0};{1};---;{2};---;{3};ERRO AO TENTAR LER DADOS DO BOLETIM OU LOG DA URNA !!!".format(UF, Municipio, Zona, Secao)

                    appendToCSV(lineToAppend, filepath_modeloUrna)

                    #Incrementa o CSV Line do modeloUrna
                    match modeloUrna:
                        case "UE2009":
                            CSVLine_UE2009 += 1
                        case "UE2010":
                            CSVLine_UE2010 += 1
                        case "UE2011":
                            CSVLine_UE2011 += 1
                        case "UE2013":
                            CSVLine_UE2013 += 1
                        case "UE2015":
                            CSVLine_UE2015 += 1
                        case "UE2020":
                            CSVLine_UE2020 += 1
                except:
                    lineToAppend = "{0};{1};---;{2};---;{3};ERRO AO TENTAR LER DADOS DO BOLETIM OU LOG DA URNA !!!".format(UF, Municipio, Zona, Secao)

                appendToCSV(lineToAppend, stdfilepath)
                CSVLine_std += 1

                #Informa conclusão desta seção
                print("Municipio: {0} Zona {1} Secao {2} concluida.".format(Municipio, Zona, Secao))