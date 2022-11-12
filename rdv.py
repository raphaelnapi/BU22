import os
import asn1

import data as Data

###########################
# EM CONSTRUÇÃO!!!

def parseRDV(UF, municipio, zona, secao):
    cod_mun = Data.getCodeMunicipio(UF, municipio)
    filename = "data\\{0}\\{1}\\o00406-{2}{3}{4}.rdv".format(UF.upper(), municipio.upper(), str(cod_mun), zona, secao)
    fileBU = open(filename, "rb")
    content = fileBU.read(os.path.getsize(filename))
    fileBU.close()
    asn1_stream = asn1.Decoder()
    asn1_stream.start(content)
    object = {}
    nodes = []
    object = ASNDecoderRDV(asn1_stream, nodes.copy())
    return object

def ObjectRDVItemName(nodes):
    list_items = {
        "[1]" : "root",
        "[1, 1]": "cabecalho",
        "[1, 1, 1]": "dataGeracao",
        "[1, 1, 2]": "idEleitoral",
        "[1, 2]": "urna",
        "[1, 2, 1]": "tipoUrna",
        "[1, 2, 2]": "versaoVotacao",
        "[1, 2, 3]": "correspondenciaResultado",
        "[1, 2, 3, 1]": "identificacao",
        "[1, 2, 3, 1, 1]": "municipioZona",
        "[1, 2, 3, 1, 1, 1]": "municipio",
        "[1, 2, 3, 1, 1, 2]": "zona",
        "[1, 2, 3, 1, 2]": "local",
        "[1, 2, 3, 1, 3]": "secao",
        "[1, 2, 3, 2]": "carga",
        "[1, 2, 3, 2, 1]": "numeroInternoUrna",
        "[1, 2, 3, 2, 2]": "numeroSerieFC",
        "[1, 2, 3, 2, 3]": "dataHoraCarga",
        "[1, 2, 3, 2, 4]": "codigoCarga",
        "[1, 2, 4]": "tipoArquivo",
        "[1, 2, 5]": "numeroSerieFV",
        "[1, 2, 6]": "motivoUtilizacaoSA",
        "[1, 2, 6, 1]": "tipoapuracao",
        "[1, 2, 6, 2]": "motivoApuracao",
        "[1, 3]": "rdv",
        "[1, 3, 1]": "pleito",
        "[1, 3, 2]": "fase",
        "[1, 3, 3]": "identificacao",
        "[1, 3, 3, 1]": "municipioZona",
        "[1, 3, 3, 1, 1]": "municipio",
        "[1, 3, 3, 1, 2]": "zona",
        "[1, 3, 3, 2]": "local",
        "[1, 3, 3, 3]": "secao",
        "[1, 3, 4]": "eleicoes",
        "[1, 3, 4, 1]": "eleicao",
        "[1, 3, 4, 1, 1]": "idEleicao",
        "[1, 3, 4, 1, 2]": "votosCargos",
        "[1, 3, 4, 1, 2, 1]": "votosCargo",
        "[1, 3, 4, 1, 2, 1, 1]": "idCargo",
        "[1, 3, 4, 1, 2, 1, 2]": "quantidadeEscolhas",
        "[1, 3, 4, 1, 2, 1, 3]": "votos",
        "[1, 3, 4, 1, 2, 1, 3, 1]": "votos",
        "[1, 3, 4, 1, 2, 1, 3, 1, 1]": "tipoVoto",
        "[1, 3, 4, 1, 2, 1, 3, 1, 2]": "digitacao",
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
    
    #Tratamento de array de votos
    split_nodes = nodes.split(",")
    nodes_count = len(split_nodes)
    if nodes_count == 8:
        item_index = (int(split_nodes[7][:-1]) - 1) + ((int(split_nodes[6]) - 3) * 10) + ((int(split_nodes[5]) - 1) * 100) + ((int(split_nodes[4]) - 2) * 1000) + ((int(split_nodes[3]) - 1) * 10000)
        return item_index
    elif nodes_count == 9:
        if split_nodes[8] == " 1]":
            nodes = "[1, 3, 4, 1, 2, 1, 3, 1, 1]" # "tipoVoto"
        elif split_nodes[8] == " 2]":
            nodes = "[1, 3, 4, 1, 2, 1, 3, 1, 2]" # "digitacao"

    if str(nodes) in list_items:
        return list_items[str(nodes)]
    else:
        return str(nodes)

def ASNDecoderRDV(asn1_stream, nodes = []):
    ret = {}

    nodes.append(1)

    while not asn1_stream.eof():
        tag = asn1_stream.peek()
        match tag.typ:
            case asn1.Types.Primitive:
                tag, value = asn1_stream.read()
                ret[ObjectRDVItemName(nodes)] = value
            case asn1.Types.Constructed:
                asn1_stream.enter()
                ret[ObjectRDVItemName(nodes)] = ASNDecoderRDV(asn1_stream, nodes.copy())
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