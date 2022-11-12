from re import T
import asn1
import os
import codecs

import data as Data
import const

#retorna dicionário a partir de arquivo BU
def parseBU(UF, municipio, zona, secao, Turno=1):
    cod_mun = Data.getCodeMunicipio(UF, municipio)

    filepath = const.urnaspath
    match Turno:
        case 1:
            filepath += "\\Turno1"
            cod_turno = const.TURNO.Primeiro
        case 2:
            filepath += "\\Turno2"
            cod_turno = const.TURNO.Segundo

    filepath += "\\{0}\\{1}".format(UF.upper(), municipio.upper())
    filepath += "\\o00{0}-{1}{2}{3}.bu".format(cod_turno, cod_mun, zona, secao)
    
    #Se não encontrar arquivo *.BU busca arquivo *.BUSA
    if not os.path.exists(filepath):
        filepath = filepath.replace(".bu", ".busa")
        #Se não encontrar *.BU nem *.BUSA retorna erro
        if not os.path.exists(filepath):
            raise Exception("File not found")

    fileBU = open(filepath, "rb")
    content = fileBU.read(os.path.getsize(filepath))
    fileBU.close()
    asn1_stream = asn1.Decoder()
    asn1_stream.start(content)
    object = {}
    nodes = []
    object = ASNDecoderBU(asn1_stream, nodes.copy())
    return object

#retorna dicionário a partir de arquivo BU
def parseBUfile(filename):
    fileBU = open(filename, "rb")
    content = fileBU.read(os.path.getsize(filename))
    fileBU.close()
    asn1_stream = asn1.Decoder()
    asn1_stream.start(content)
    object = {}
    nodes = []
    object = ASNDecoderBU(asn1_stream, nodes.copy())
    return object

#utilizado para dar o nome correto das chaves do dicionário BU
def ObjectBUItemName(nodes):
    list_items = {
        "[1]": "root",
        "[1, 1]": "cabecalho",
        "[1, 1, 1]": "dataGeracao",
        "[1, 1, 2]": "idEleitoral",
        "[1, 2]": "fase",
        "[1, 3]": "identificacao",
        "[1, 3, 1]": "municipioZona",
        "[1, 3, 1, 1]": "municipio",
        "[1, 3, 1, 2]": "zona",
        "[1, 3, 2]": "local",
        "[1, 3, 3]": "secao",
        "[1, 4]": "tipoEnvelope",
        "[1, 5]": "conteudo",
        "[1, 5, 1]": "entidadeBoletimUrna",
        "[1, 5, 1, 1]": "cabecalho",
        "[1, 5, 1, 1, 1]": "dataGeracao",
        "[1, 5, 1, 1, 2]": "idEleitoral",
        "[1, 5, 1, 2]": "fase",
        "[1, 5, 1, 3]": "urna",
        "[1, 5, 1, 3, 1]": "tipoUrna",
        "[1, 5, 1, 3, 2]": "versaoVotacao",
        "[1, 5, 1, 3, 3]": "correspondenciaResultado",
        "[1, 5, 1, 3, 3, 1]": "identificacao",
        "[1, 5, 1, 3, 3, 1, 1]": "municipioZona",
        "[1, 5, 1, 3, 3, 1, 1, 1]": "municipio",
        "[1, 5, 1, 3, 3, 1, 1, 2]": "zona",
        "[1, 5, 1, 3, 3, 1, 2]": "local",
        "[1, 5, 1, 3, 3, 1, 3]": "secao",
        "[1, 5, 1, 3, 3, 2]": "carga",
        "[1, 5, 1, 3, 3, 2, 1]": "numeroInternoUrna",
        "[1, 5, 1, 3, 3, 2, 2]": "numeroSerieFC",
        "[1, 5, 1, 3, 3, 2, 3]": "dataHoraCarga",
        "[1, 5, 1, 3, 3, 2, 4]": "codigoCarga",
        "[1, 5, 1, 3, 4]": "tipoArquivo",
        "[1, 5, 1, 3, 5]": "numeroSerieFV",
        "[1, 5, 1, 3, 6]": "motivoUtilizacaoSA",
        "[1, 5, 1, 3, 6, 1]": "tipoapuracao",
        "[1, 5, 1, 3, 6, 2]": "motivoApuracao",
        "[1, 5, 1, 4]": "identificacao",
        "[1, 5, 1, 4, 1]": "municipioZona",
        "[1, 5, 1, 4, 1, 1]": "municipio",
        "[1, 5, 1, 4, 1, 2]": "zona",
        "[1, 5, 1, 4, 2]": "local",
        "[1, 5, 1, 4, 3]": "secao",
        "[1, 5, 1, 5]": "dataHoraEmissao",
        "[1, 5, 1, 6]": "dadosSecao/dadosSA",
        "[1, 5, 1, 6, 1]": "dataHoraAbertura/juntaApuradora",
        "[1, 5, 1, 6, 2]": "dataHoraEncerramento/turmaApuradora",
        "[1, 5, 1, 6, 3]": "dataHoraDesligamentoVotoImpresso/numeroInternoUrnaOrigem",
        "[1, 5, 1, 7]": "qtdEleitoresLibCodigo",
        "[1, 5, 1, 8]": "qtdEleitoresCompBiometrico",
        "[1, 5, 1, 9]": "resultadosVotacaoPorEleicao",
        "[1, 5, 1, 9, 1]": "resultadosVotacaoPorEleicao",
        "[1, 5, 1, 9, 1, 1]": "idEleicao",
        "[1, 5, 1, 9, 1, 2]": "qtdEleitoresAptos",
        "[1, 5, 1, 9, 1, 3]": "resultadosVotacao",
        "[1, 5, 1, 9, 1, 3, 1]": "resultadosVotacao",
        "[1, 5, 1, 9, 1, 3, 1, 1]": "tipoCargo",
        "[1, 5, 1, 9, 1, 3, 1, 2]": "qtdComparecimento",
        "[1, 5, 1, 9, 1, 3, 1, 3]": "totaisVotosCargo",
        "[1, 5, 1, 9, 1, 3, 1, 3, 1]": "totaisVotosCargo",
        "[1, 5, 1, 9, 1, 3, 1, 3, 1, 1]": "codigoCargoConsulta",
        "[1, 5, 1, 9, 1, 3, 1, 3, 1, 2]": "ordemImpressao",
        "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3]": "votosVotaveis",
        "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1]": "votosVotaveis",
        "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1, 1]": "tipoVoto",
        "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1, 2]": "quantidadeVotos",
        "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1, 3]": "identificacaoVotavel",
        "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1, 3, 1]": "partido",
        "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1, 3, 2]": "codigo",
        "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1, 4]": "assinatura",
        "[1, 5, 1, 10]": "historicoCorrespondencias",
        "[1, 5, 1, 11]": "historicoVotoImpresso",
        "[1, 5, 1, 12]": "chaveAssinaturaVotosVotavel"
    }
        
    IDEleitoral = {
        "[1]":"IDProcessoEleitoral",
        "":"IDPleito",
        "[3]":"IDEleicao"
    }
    
    TipoUrna = {
        1:"secao",
        3:"contingencia",
        4:"reservaSecao",
        6:"reservaEncerrandoSecao"
    }
    
    TipoArquivo = {
        1:"votacaoUE",
        2:"votacaoRED",
        3:"saMistaMRParcialCedula",
        4:"saMistaBUImpressoCedula",
        5:"saManual",
        6:"saEletronica"
    }
    
    TipoApuracaoSA = {
        "[0]":"ApuracaoMistaMR",
        "[1]":"ApuracaoMistaBUAE",
        "":"ApuracaoTotalmenteManualDigitacaoAE",
        "[3]":"ApuracaoEletronica"
    }
    
    Fase = {
        1:"simulado",
        2:"oficial",
        3:"treinamento"
    }
    
    TipoEnvelope = {
        1:"envelopeBoletimUrna",
        2:"envelopeRegistroDigitalVoto",
        4:"envelopeBoletimUrnaImpresso",
        5:"envelopeImagemBiometria"
    }
    
    TipoVoto = {
        1:"nominal",
        2:"branco",
        3:"nulo",
        4:"legenda",
        5:"cargoSemCandidato"
    }
    
    TipoCargoConsulta = {
        1:"majoritario",
        2:"proporcional",
        3:"consulta"
    }
    
    Eleicoes = {
        "[1]":"EleicaoVota",
        "":"EleicaoSA"
    }

    CodigoCargoConsulta = {
        "[1]":"CargoConstitucional",
        "":"NumeroCargoConsultaLivre"
    }

    CargoConstitucional = {
        1:"Presidente",
        2:"Vice-Presidente",
        3:"Governador",
        4:"Vice-Governador",
        5:"Senador",
        6:"Deputado Federal",
        7:"Deputado Estadual",
        8:"Deputado Distrital",
        9:"1 Suplente Senador",
        10:"2 Suplente Senador",
        11:"Prefeito",
        12:"Vice-Prefeito",
        13:"Vereador"
    }
    
    TipoCedulaSA = {
        1:"majoritario",
        2:"proporcional"
    }
    
    OrigemVotosSA = {
        1:"cedula",
        2:"rdv",
        3:"bu"
    }
    
    TipoApuracao = {
        1:"totalmenteManual",
        2:"totalmenteEletronica",
        3:"mistaBU",
        4:"mistaMR"
    }
    
    MotivoApuracaoManual = {
        1:"urnaComDefeito",
        2:"urnaIndisponivelInicio",
        3:"urnaOutraSecao",
        99:"outros"
    }
    
    MotivoApuracaoMistaComMR = {
        1:"naoObteveExitoContingencia",
        2:"indisponibilidadeUrnaContingencia",
        3:"indisponibilidadeFlashContingencia",
        4:"problemaEnergiaEletrica",
        5:"naoFoiPossivelTrocarUrna",
        6:"naoFoiSolicitadaTrocaUrna",
        99:"outros"
    }
    
    MotivoApuracaoMistaComBU = {
        1:"urnaDataHoraIncorreta",
        2:"urnaComDefeito",
        3:"urnaOutrasecao",
        4:"urnaPreparadaIncorretamente",
        5:"urnaChegouAposInicioVotacao",
        99:"outros"
    }
    
    MotivoApuracaoEletronica = {
        1:"naoFoiPossivelReuperarResultado",
        2:"urnaNaoChegouMidiaDefeituosa",
        3:"urnaNaoChegouMidiaExtraviada",
        99:"outros"
    }

    nodes = str(nodes)
    
    #Tratamento de array 
    #"[1, 5, 1, 9, 1]": "resultadosVotacaoPorEleicao",
    #    "[1, 5, 1, 9, 1, 1]": "idEleicao",
    #    "[1, 5, 1, 9, 1, 2]": "qtdEleitoresAptos",
    #    "[1, 5, 1, 9, 1, 3]": "resultadosVotacao",
    ##    "[1, 5, 1, 9, 1, 3, 1]": "resultadosVotacao",
     #   "[1, 5, 1, 9, 1, 3, 1, 1]": "tipoCargo",
     #   "[1, 5, 1, 9, 1, 3, 1, 2]": "qtdComparecimento",
     ##   "[1, 5, 1, 9, 1, 3, 1, 3]": "totaisVotosCargo",
      #  "[1, 5, 1, 9, 1, 3, 1, 3, 1]": "totaisVotosCargo",
      #  "[1, 5, 1, 9, 1, 3, 1, 3, 1, 1]": "codigoCargoConsulta",
      #  "[1, 5, 1, 9, 1, 3, 1, 3, 1, 2]": "ordemImpressao",
       # "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3]": "votosVotaveis",
    #"[1, 5, 1, 9, 1, 3, 1]": "resultadosVotacao",

    #Tratamento de array
    split_nodes = nodes.split(",")
    nodes_count = len(split_nodes)

    if nodes[:11] == "[1, 5, 1, 9": #resultadosVotacaoPorEleicao
        if nodes_count == 5:
            item_index = (int(split_nodes[4][:-1]) - 1)
            return item_index
        elif nodes_count > 5:
            split_nodes[4] = " 1"
            nodes = ",".join(split_nodes)

    if nodes[:17] == "[1, 5, 1, 9, 1, 3": #resultadosVotacao
        if nodes_count == 7:
            item_index = (int(split_nodes[6][:-1]) - 1)
            return item_index
        elif nodes_count > 7:
            split_nodes[6] = " 1"
            nodes = ",".join(split_nodes)

    if nodes[:23] == "[1, 5, 1, 9, 1, 3, 1, 3": #totaisVotosCargo
        if nodes_count == 9:
            item_index = (int(split_nodes[8][:-1]) - 1)
            return item_index
        elif nodes_count > 9:
            split_nodes[8] = " 1"
            nodes = ",".join(split_nodes)

    #Array de votosVotaveis [1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1]
    if nodes_count == 11:
        item_index = (int(split_nodes[10][:-1]) - 1) + ((int(split_nodes[9]) - 3) * 10) + ((int(split_nodes[8]) - 1) * 100) + ((int(split_nodes[7]) - 3) * 1000) + ((int(split_nodes[6]) - 1) * 10000) + ((int(split_nodes[5]) - 3) * 100000) + ((int(split_nodes[4]) - 1) * 1000000)
        return item_index
    elif nodes_count == 12:
        if split_nodes[11] == " 1]":
            nodes = "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1, 1]" #"tipoVoto"
        elif split_nodes[11] == " 2]":
            nodes = "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1, 2]" #"quantidadeVotos"
        elif split_nodes[11] == " 3]":
            nodes = "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1, 3]" #"identificacaoVotavel"
        elif split_nodes[11] == " 4]":
            nodes = "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1, 4]" #"assinatura"
    elif nodes_count == 13:
        if split_nodes[12] == " 1]":
            nodes = "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1, 3, 1]" #"partido"
        elif split_nodes[12] == " 2]":
            nodes = "[1, 5, 1, 9, 1, 3, 1, 3, 1, 3, 1, 3, 2]" #"codigo"

    if str(nodes) in list_items:
        return list_items[str(nodes)]
    else:
        return str(nodes)

def ASNDecoderBU(asn1_stream, nodes = []):
    ret = {}

    nodes.append(1)

    while not asn1_stream.eof():
        tag = asn1_stream.peek()
        match tag.typ:
            case asn1.Types.Primitive:
                tag, value = asn1_stream.read()
                if str(nodes) == "[1, 5]": #conteudo
                    asn1_stream2 = asn1.Decoder()
                    asn1_stream2.start(value)
                    ret[ObjectBUItemName(nodes)] = ASNDecoderBU(asn1_stream2, nodes.copy())
                else:
                    ret[ObjectBUItemName(nodes)] = value
            case asn1.Types.Constructed:
                asn1_stream.enter()
                ret[ObjectBUItemName(nodes)] = ASNDecoderBU(asn1_stream, nodes.copy())
                asn1_stream.leave()
            case _:
                ret["Erro"] = "Dado inesperado"

        nodes[len(nodes) - 1] += 1

    return ret

def ASNType(type):
    match type:
        case 0x01:
            return "Boolean"
        case 0x02:
            return "Integer"
        case 0x04:
            return "OctetString"
        case 0x05:
            return "Null"
        case 0x06:
            return "ObjectIdentifier"
        case 0x0a:
            return "Enumerated"
        case 0x10:
            return "Sequence"
        case 0x11:
            return "Set"
        case _:
            return "Unknown"


class objBU:
    dict = {}
    UF = ""
    Municipio = ""
    Secao = ""
    indexResultadosVotacaoPorEleicao = 0

    def __init__(self, UF, Municipio, Zona, Secao, Turno=1):
        self.UF = UF
        self.Municipio = Municipio
        self.Secao = Secao
        if Turno == 1:
            indexResultadosVotacaoPorEleicao = 1
        elif Turno == 2:
            indexResultadosVotacaoPorEleicao = 0
        self.dict = parseBU(UF, Municipio, Zona, Secao, Turno)

    def getQtdEleitoresAptos(self):
        return int(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["resultadosVotacaoPorEleicao"][self.indexResultadosVotacaoPorEleicao]["qtdEleitoresAptos"])

    def getQtdComparecimento(self):
        return int(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["resultadosVotacaoPorEleicao"][self.indexResultadosVotacaoPorEleicao]["resultadosVotacao"][0]["qtdComparecimento"])

    def getQtdCandidatos(self):
        return len(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["resultadosVotacaoPorEleicao"][self.indexResultadosVotacaoPorEleicao]["resultadosVotacao"][0]["totaisVotosCargo"][0]["votosVotaveis"] - 2) #-2 para retirar branco e nulo

    def getVotosCandidato(self, index):
        return int.from_bytes(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["resultadosVotacaoPorEleicao"][self.indexResultadosVotacaoPorEleicao]["resultadosVotacao"][0]["totaisVotosCargo"][0]["votosVotaveis"][index]["quantidadeVotos"], "big")

    def getCodigoCandidato(self, index):
        return int(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["resultadosVotacaoPorEleicao"][self.indexResultadosVotacaoPorEleicao]["resultadosVotacao"][0]["totaisVotosCargo"][0]["votosVotaveis"][index]["identificacaoVotavel"]["codigo"])

    def getTipoVoto(self, index):
        return int.from_bytes(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["resultadosVotacaoPorEleicao"][self.indexResultadosVotacaoPorEleicao]["resultadosVotacao"][0]["totaisVotosCargo"][0]["votosVotaveis"][index]["tipoVoto"], "big")

    def getVotosBrancos(self):
        return int.from_bytes(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["resultadosVotacaoPorEleicao"][self.indexResultadosVotacaoPorEleicao]["resultadosVotacao"][0]["totaisVotosCargo"][0]["votosVotaveis"][5]["quantidadeVotos"], "big")

    def getVotosNulos(self):
        return int.from_bytes(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["resultadosVotacaoPorEleicao"][self.indexResultadosVotacaoPorEleicao]["resultadosVotacao"][0]["totaisVotosCargo"][0]["votosVotaveis"][6]["quantidadeVotos"], "big")

    def getHoraAbertura(self):
        return self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["dadosSecao/dadosSA"]["dataHoraAbertura/juntaApuradora"].decode("utf8")

    def getHoraEncerramento(self):
        return self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["dadosSecao/dadosSA"]["dataHoraEncerramento/turmaApuradora"].decode("utf8")

    def getHoraEmissao(self):
        return self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["dataHoraEmissao"].decode("utf8")

    def getQtdEleitoresCompBiometrico(self):
        return int.from_bytes(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["qtdEleitoresCompBiometrico"], "big")

    def getTipoUrna(self):
        return int(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["urna"]["tipoUrna"])

    def getVersaoVotacao(self):
        return self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["urna"]["versaoVotacao"].decode("ansi")

    def getNumeroInternoUrna(self):
        return str(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["urna"]["correspondenciaResultado"]["carga"]["numeroInternoUrna"])

    def getNumeroSerieFC(self):
        return int.from_bytes(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["urna"]["correspondenciaResultado"]["carga"]["numeroSerieFC"], "big")

    def getNumeroSerieFV(self):
        return int.from_bytes(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["urna"]["numeroSerieFV"], "big")
        

    def getMunicipioCode(self):
        return int(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["urna"]["correspondenciaResultado"]["identificacao"]["municipioZona"]["municipio"])

    def getZona(self):
        return int(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["urna"]["correspondenciaResultado"]["identificacao"]["municipioZona"]["zona"])

    def getLocal(self):
        if "local" in self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["urna"]["correspondenciaResultado"]["identificacao"].keys():
            return int(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["urna"]["correspondenciaResultado"]["identificacao"]["local"])
        else:
            return "-"

    def getSecao(self):
        if "secao" in self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["urna"]["correspondenciaResultado"]["identificacao"].keys():
            return int(self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["urna"]["correspondenciaResultado"]["identificacao"]["secao"])
        else:
            return self.Secao + " (não consta no BU)"


    def getDataHoraCarga(self):
        return self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["urna"]["correspondenciaResultado"]["carga"]["dataHoraCarga"].decode("utf8")

    def getCodigoCarga(self):
        return self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["urna"]["correspondenciaResultado"]["carga"]["codigoCarga"].decode("utf8")

    def getSetCandidatos(self):
        return self.dict["root"]["conteudo"]["entidadeBoletimUrna"]["resultadosVotacaoPorEleicao"][self.indexResultadosVotacaoPorEleicao]["resultadosVotacao"][0]["totaisVotosCargo"][0]["votosVotaveis"]

    def getDictVotos(self):
        votos = {  
            12: 0,
            13: 0,
            14: 0,
            15: 0,
            16: 0,
            21: 0,
            22: 0,
            27: 0,
            30: 0,
            44: 0,
            80: 0,
            "branco": 0,
            "nulo": 0
        }
        for objCandidato in self.getSetCandidatos().values():
            if objCandidato["tipoVoto"] == b'\x01': #Presidente
                votos[objCandidato["identificacaoVotavel"]["codigo"]] = int.from_bytes(objCandidato["quantidadeVotos"], "big")
            elif objCandidato["tipoVoto"] == b'\x02': #Branco
                    votos["branco"] = int.from_bytes(objCandidato["quantidadeVotos"], "big")
            elif objCandidato["tipoVoto"] == b'\x03': #Nulo
                votos["nulo"] = int.from_bytes(objCandidato["quantidadeVotos"], "big")

        return votos

    def toCSV(self, CSVLine = 2):
        dictVotos = self.getDictVotos()
        strVotos = str(dictVotos).replace("{", "").replace("}", "").replace(":", ";").replace(",", ";")
        cols = []
        cols.append(str(self.UF))
        cols.append(self.Municipio)
        cols.append(str(self.getMunicipioCode()))
        cols.append(str(self.getZona()))
        cols.append(str(self.getLocal()))
        cols.append(str(self.getSecao()))
        cols.append(str(self.getDataHoraCarga()))
        cols.append(str(self.getCodigoCarga()))
        cols.append(str(self.getNumeroSerieFC()))
        cols.append(str(self.getNumeroSerieFV()))
        cols.append(str(self.getNumeroInternoUrna()))
        cols.append(str(self.getVersaoVotacao()))
        cols.append(str(self.getTipoUrna()))
        cols.append(str(self.getQtdEleitoresAptos()))
        cols.append(str(self.getQtdComparecimento()))
        cols.append("=O{0}-AW{0}-AY{0}".format(CSVLine)) #votos validos
        cols.append("=P{0}".format(CSVLine) if CSVLine == 2 else "=P{0}+Q{1}".format(CSVLine, CSVLine - 1)) #soma de votos validos
        cols.append(str(self.getQtdEleitoresCompBiometrico()))
        cols.append(str(self.getQtdEleitoresAptos() - self.getQtdComparecimento()))
        
        for cod_candidato in dictVotos.keys():
            cols.append(str(cod_candidato))
            cols.append(str(dictVotos[cod_candidato]))
            if cod_candidato == 13:
                cols.append("=W{0}*100/P{0}".format(CSVLine)) #percentual
                cols.append("=W{0}".format(CSVLine) if CSVLine == 2 else "=W{0}+Y{1}".format(CSVLine, CSVLine - 1)) #soma
                cols.append("=Y{0}*100/Q{0}".format(CSVLine)) #percentual crescimento
            elif cod_candidato == 22:
                cols.append("=AJ{0}*100/P{0}".format(CSVLine)) #percentual
                cols.append("=AJ{0}".format(CSVLine) if CSVLine == 2 else "=AJ{0}+AL{1}".format(CSVLine, CSVLine - 1)) #soma
                cols.append("=AL{0}*100/Q{0}".format(CSVLine)) #percentual crescimento

        cols.append(str(self.getHoraAbertura()))
        cols.append(str(self.getHoraEncerramento()))
        cols.append(str(self.getHoraEmissao()))
        ret = ";".join(cols)
        #ret = str(self.UF) + ";" + self.Municipio + ";" + str(self.getMunicipio()) + ";" + str(self.getZona()) + ";" + str(self.getLocal()) + ";" + str(self.getSecao()) + ";" + str(self.getDataHoraCarga()) + ";" + str(self.getCodigoCarga()) + ";" + str(self.getNumeroSerieFC()) + ";" + str(self.getNumeroSerieFV()) + ";" + str(self.getNumeroInternoUrna()) + ";" + str(self.getVersaoVotacao()) + ";" + str(self.getTipoUrna()) + ";" + str(self.getQtdEleitoresAptos()) + ";=Q{0}-AW{0}-AY{0};".format(self.CSVLine) + ("P{0}".format(self.CSVLine) if self.CSVLine == 2 else "P{0}-Q{1}".format(self.CSVLine, self.CSVLine - 1)) + ";" + str(self.getQtdComparecimento()) + ";" + str(self.getQtdEleitoresCompBiometrico()) + ";" + str(self.getQtdEleitoresAptos() - self.getQtdComparecimento()) + ";" + strVotos  + ";" + str(self.getHoraAbertura()) + ";" + str(self.getHoraEncerramento()) + ";" + str(self.getHoraEmissao())
        return ret
