import shutil
import os
import py7zr
import time
import datetime
import sys

import data as Data

def parseLog(UF, Municipio, Zona, Secao):
    cod_mun = Data.getCodeMunicipio(UF, Municipio)
    filename = "data\\{0}\\{1}\\o00406-{2}{3}{4}.logjez".format(UF.upper(), Municipio.upper(), str(cod_mun), Zona, Secao)
    parseLogFilename(filename)

def parseLogFilename(filename):
    #Se não encontrar arquivo *.LOGJEZ busca arquivo *.LOGSAJEZ
    if not os.path.exists(filename):
        filename = filename.replace(".logjez", ".logsajez")
        #Se não encontrar *.LOGJEZ nem *.LOGSAJEZ retorna erro
        if not os.path.exists(filename):
            raise Exception("File not found")

    temp_dir = "data\\temp\\"

    #descompactar
    descompactar7zip(filename, temp_dir)

    #lê o arquivo
    dictLog = leLogd(temp_dir + "logd.dat")

    arquivos_temporarios = os.listdir(temp_dir)

    #carrega Log de urna de contingência
    #melhorar: ler o nome do arquivo no Log da primeira urna em vez de buscar qualquer arquivo .jez
    for arquivo in arquivos_temporarios:
        if arquivo.split(".")[1] == "jez":
            descompactar7zip(temp_dir + arquivo, temp_dir)
            dictLog.extend(leLogd(temp_dir + "logd.dat"))

    for arquivo in arquivos_temporarios:
        os.remove(temp_dir + arquivo)

    return dictLog

def descompactar7zip(filename, extract_dir):
    file7zip = py7zr.SevenZipFile(filename, "r")
    file7zip.extractall(extract_dir)
    file7zip.close()

def leLogd(filename):
    dictLog = []
    file = open(filename, "rt")
    line = "x"
    line_count = 1
    while line:
        try:
            line = file.readline()
            if line != "":
                dictLine = {}
                data = line.split("\t")
                dictLine["datahora"] = data[0].strip()
                dictLine["info"] = data[1].strip()
                dictLine["numero"] = data[2].strip()
                dictLine["interface"] = data[3].strip()
                dictLine["mensagem"] = data[4].strip()
                dictLine["assinatura"] = data[5].strip()
                dictLog.append(dictLine)
                line_count += 1
        except:
            print("Erro ao ler a  linha {0}\nDetalhes: {1}".format(line_count, sys.exc_info()))
            
    file.close()
    return dictLog

class objLog:
    dict = []
    UF = ""
    Municipio = ""
    Secao = ""

    def __init__(self, UF, Municipio, Zona, Secao):
        #falta:
        #   identificar se tiver mais de um arquivo compactado (outro Log compactado dentro do primeiro)
        #       nesse caso acrescentar as linhas do outro arquivo (identificar sequencia pelo campo DataHora)
        self.UF = UF
        self.Municipio = Municipio
        self.Secao = Secao
        self.dict = parseLog(UF, Municipio, Zona, Secao)

    def getQtdEleitoresVotaram(self):
        return self._getQtdDado("mensagem", "O voto do eleitor foi computado")

    def getQtdTituloInvalido(self):
        return self._getQtdDado("mensagem", "Título inválido")

    def getQtdEleitorJaVotou(self):
        return self._getQtdDado("mensagem", "O eleitor identificado já votou")

    def getQtdNaoPossuiBiometria(self):
        return self._getQtdDado("mensagem", "O eleitor não possui biometria")

    def getQtdMesarioIndagadoSeEleitorVotando(self):
        return self._getQtdDado("mensagem", "Mesário indagado se eleitor está votando")

    def urnaTestada(self):
        if self._getQtdDado("mensagem", "Urna não testada"):
            return 0
        else:
            return 1

    def getQtdTentativaVoto(self):
        return self._getQtdDado("mensagem", "Título digitado pelo mesário")

    def getQtdTipoHabilitacao(self):
        biometrica = 0
        sem_biometria = 0
        biometria_falhou = 0

        for i in range(0, len(self.dict)):
            if self.dict[i]["mensagem"] == "Eleitor foi habilitado":

                #encontra mensagem que corresponde ao tipo de habilitação (pula mensagens relacionadas a fone de ouvido)
                mensagem = ""
                varredura_encontra_habilitacao = 0
                while mensagem != "Tipo de habilitação do eleitor [biométrica]" and mensagem != "Capturada a digital do mesário" and mensagem != "O eleitor não possui biometria":
                    varredura_encontra_habilitacao += 1
                    mensagem = self.dict[i - varredura_encontra_habilitacao]["mensagem"]

                #incrementa cada tipo de habilitação encontrada
                match mensagem:
                    case "Tipo de habilitação do eleitor [biométrica]":
                        biometrica += 1
                    case "Capturada a digital do mesário":
                        biometria_falhou += 1
                    case "O eleitor não possui biometria":
                        sem_biometria += 1
                    case _:
                        print("Novo tipo de habilitação encontrado: {0}".format(mensagem))

        return {
            "biometrica": biometrica,
            "sem_biometria": sem_biometria,
            "biometria_falhou": biometria_falhou
        }

    def getMediaIntervaloEntreEleitores(self):
        qtd_intervalo = 0
        soma_intervalo = datetime.timedelta()
        for Linha in self.dict:
            if Linha["mensagem"] == "Aguardando digitação do título":
                time1 = time.strptime(Linha["datahora"], "%d/%m/%Y %H:%M:%S")
                #print(time1.__str__())
            elif Linha["mensagem"] == "Título digitado pelo mesário":
                time2 = time.strptime(Linha["datahora"], "%d/%m/%Y %H:%M:%S")
                #print(time2.__str__())
                delta1 = datetime.timedelta(hours=time1.tm_hour, minutes=time1.tm_min, seconds=time1.tm_sec)
                delta2 = datetime.timedelta(hours=time2.tm_hour, minutes=time2.tm_min, seconds=time2.tm_sec)
                intervalo = (delta2 - delta1)
                #print(str(intervalo))
                soma_intervalo += intervalo
                qtd_intervalo += 1

        return soma_intervalo / qtd_intervalo
                
    def getMaiorIntervaloEntreEleitores(self):
        ret = datetime.timedelta()
        for Linha in self.dict:
            if Linha["mensagem"] == "Aguardando digitação do título":
                time1 = time.strptime(Linha["datahora"], "%d/%m/%Y %H:%M:%S")
                #print(time1.__str__())
            elif Linha["mensagem"] == "Título digitado pelo mesário":
                time2 = time.strptime(Linha["datahora"], "%d/%m/%Y %H:%M:%S")
                #print(time2.__str__())
                delta1 = datetime.timedelta(hours=time1.tm_hour, minutes=time1.tm_min, seconds=time1.tm_sec)
                delta2 = datetime.timedelta(hours=time2.tm_hour, minutes=time2.tm_min, seconds=time2.tm_sec)
                intervalo = (delta2 - delta1)
                if intervalo > ret: ret = intervalo
                #print(str(intervalo))

        return ret

    def getIntervalosEntreEleitores(self):
        ret = []
        for Linha in self.dict:
            if Linha["mensagem"] == "Aguardando digitação do título":
                time1 = time.strptime(Linha["datahora"], "%d/%m/%Y %H:%M:%S")
                #print(time1.__str__())
            elif Linha["mensagem"] == "Título digitado pelo mesário":
                time2 = time.strptime(Linha["datahora"], "%d/%m/%Y %H:%M:%S")
                #print(time2.__str__())
                delta1 = datetime.timedelta(hours=time1.tm_hour, minutes=time1.tm_min, seconds=time1.tm_sec)
                delta2 = datetime.timedelta(hours=time2.tm_hour, minutes=time2.tm_min, seconds=time2.tm_sec)
                intervalo = (delta2 - delta1)
                ret.append(str(intervalo))

        return ret

    def _getQtdDado(self, chave, valor):
        ret = 0
        for Linha in self.dict:
            if Linha[chave] == valor:
                ret += 1
        
        return ret

    def printAlertas(self):
        for Linha in self.dict:
            if Linha["info"] == "ALERTA":
                print(Linha["mensagem"])

    def toCSV(self):
        TipoHabilitacao = self.getQtdTipoHabilitacao()
        ret = TipoHabilitacao["biometrica"].__str__() + "; " + TipoHabilitacao["sem_biometria"].__str__() + "; " + TipoHabilitacao["biometria_falhou"].__str__() + "; " + self.getQtdEleitoresVotaram().__str__() + "; " + self.getQtdTentativaVoto().__str__() + "; " + self.getQtdTituloInvalido().__str__() + "; " + self.getQtdMesarioIndagadoSeEleitorVotando().__str__() + "; " + self.getQtdEleitorJaVotou().__str__() + "; " + self.getMediaIntervaloEntreEleitores().__str__() + "; " + self.getMaiorIntervaloEntreEleitores().__str__()
        return ret