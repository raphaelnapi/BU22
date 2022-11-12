import os
import requests
import json

from const import HASH

import data as Data
import const

def registraListas():
    #ret = 0
    for UF in Data.Estados.keys():
        Municipios = Data.getMunicipios(UF)
        for Municipio in Municipios:
            Zonas = Data.getZonas(UF, Municipio)
            for Zona in Zonas:
                Secoes = getSecoes(UF, Municipio, Zona)
                Data.salvaArquivo(Secoes.__str__().replace("[", "").replace("]", "").replace(", ", ";").replace("'", ""), "{0}\\listas\\Secoes_{1}_{2}_{3}.dat".format(const.datapath, UF,  Municipio, Zona))

                print("{0}\\{1}\\{2}".format(UF, Municipio, Zona) + " ok.")
                #ret += len(Secoes)
                #print(ret)

def downloadMunicipiosJSON():
    response = requests.get("https://resultados.tse.jus.br/oficial/ele2022/544/config/mun-e000544-cm.json")
    
    Data.criaPastaData()

    file = open("{0}\\MunicipiosJSON.dat".format(const.datapath), "wt")
    file.write(response.text)
    file.close()

def getSecoes(UF, municipio, zona):
    ret = []
    cdmun = Data.getCodeMunicipio(UF, municipio)

    try:
        response = requests.get("https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/406/config/{0}/{0}-p000406-cs.json".format(UF.lower()), timeout = 60)
    except:
        return getSecoes(UF, municipio, zona)
    dados = json.loads(response.text)
    for mun in dados["abr"][0]["mu"]:
        if mun["cd"] == cdmun:
            for zon in mun["zon"]:
                if int(zon["cd"]) == int(zona):
                    for Secao in zon["sec"]:
                        ret.append(Secao["ns"])

    return ret

def getHashes(UF, municipio, zona, secao, Turno = const.TURNO.Primeiro):
    if str(municipio).isdigit():
        cdmun = municipio
    else:
        cdmun = Data.getCodeMunicipio(UF, municipio)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get("https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/{0}/dados/{1}/{2}/{3}/{4}/p000{0}-{1}-m{2}-z{3}-s{4}-aux.json".format(Turno, UF.lower(), cdmun, zona, secao))
    except:
        return getHashes(UF, municipio, zona, secao, Turno)
    #print("https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/{0}/dados/{1}/{2}/{3}/{4}/p000{0}-{1}-m{2}-z{3}-s{4}-aux.json".format(Turno, UF.lower(), cdmun, zona, secao))
    #print(response.text)
    response_json = json.loads(response.text)
    hashes = json.loads(json.dumps(response_json["hashes"][0]))
    filebu = ""
    filerdv = ""
    filelog = ""
    #print("{0} {1} {2} {3}".format(UF, municipio, zona, secao))
    for nmarq in hashes["nmarq"]:
        match nmarq.split(".")[1]:
            case "bu" | "busa":
                filebu = nmarq
            case "rdv":
                filerdv = nmarq
            case "logjez" | "logsajez":
                filelog = nmarq
    #print(hashes)
    return hashes["hash"], filebu, filelog, filerdv

def downloadFiles(UF, Municipio, cod_mun, Zona, Secao, downloaddir=const.urnaspath, cod_turno = const.TURNO.Primeiro):
    hashes = getHashes(UF.upper(), cod_mun, Zona, Secao, cod_turno)

    downloadBU(UF, cod_mun, Zona, Secao, hashes, downloaddir, cod_turno)
    downloadRDV(UF, cod_mun, Zona, Secao, hashes, downloaddir, cod_turno)
    downloadLOG(UF, cod_mun, Zona, Secao, hashes, downloaddir, cod_turno)


def downloadBU(UF, cod_mun, zona, secao, hashes, downloaddir=const.urnaspath, cod_turno = const.TURNO.Primeiro):
    filepath = downloaddir + hashes[HASH.Bu]
    #if not os.path.isfile(filepath):
    try:
        response = requests.get("https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/{0}/dados/{1}/{2}/{3}/{4}/{5}/{6}".format(cod_turno, UF.lower(), cod_mun, zona, secao, hashes[HASH.Hash], hashes[HASH.Bu]))
        file = open(filepath, "wb")
        file.write(response.content)
        file.close()
        #print("{0} baixado.".format(hashes[HASH.Bu]))
    except:
        downloadBU(UF, cod_mun, zona, secao, hashes, downloaddir, cod_turno)

def downloadRDV(UF, cod_mun, zona, secao, hashes, downloaddir="", cod_turno = const.TURNO.Primeiro):
    filepath = downloaddir + hashes[HASH.Rdv]
    #if not os.path.isfile(filepath):
    try:
        response = requests.get("https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/{0}/dados/{1}/{2}/{3}/{4}/{5}/{6}".format(cod_turno, UF.lower(), cod_mun, zona, secao, hashes[HASH.Hash], hashes[HASH.Rdv]))
        file = open(filepath, "wb")
        file.write(response.content)
        file.close()
        #print("{0} baixado.".format(hashes[HASH.Rdv]))
    except:
        downloadRDV(UF, cod_mun, zona, secao, hashes, downloaddir, cod_turno)

def downloadLOG(UF, cod_mun, zona, secao, hashes, downloaddir="", cod_turno = const.TURNO.Primeiro):
    filepath = downloaddir + hashes[HASH.Logjez]
    #if not os.path.isfile(filepath):
    try:
        response = requests.get("https://resultados.tse.jus.br/oficial/ele2022/arquivo-urna/{0}/dados/{1}/{2}/{3}/{4}/{5}/{6}".format(cod_turno, UF.lower(), cod_mun, zona, secao, hashes[HASH.Hash], hashes[HASH.Logjez]))
        file = open(filepath, "wb")
        file.write(response.content)
        file.close()
        #print("{0} baixado.".format(hashes[HASH.Logjez]))
    except:
        downloadLOG(UF, cod_mun, zona, secao, hashes, downloaddir, cod_turno)

def downloadDatafromUF(UF, Turno = 1):
    print("Realizando download de arquivos de " + UF + "\n\n")

    #Diretorio de download
    downloaddir_root = const.urnaspath
    cod_turno = 0
    match Turno:
        case 1:
            cod_turno = const.TURNO.Primeiro
            downloaddir_root += "\\Turno1"
        case 2:
            cod_turno = const.TURNO.Segundo
            downloaddir_root += "\\Turno2"

    Municipios = Data.getMunicipios(UF)

    #calcula progresso_total
    progresso_total = 0
    for Municipio in Municipios:
        Zonas = Data.getZonas(UF, Municipio)
        progresso_total += len(Zonas)

    #faz download
    progresso = 0
    for Municipio in Municipios:
        Data.criaPastaMunicipio(UF, Municipio, downloaddir_root)
        cod_mun = Data.getCodeMunicipio(UF, Municipio)
        Zonas = Data.getZonas(UF, Municipio)
        for Zona in Zonas:
            Secoes = Data.getSecoes(UF, Municipio, Zona)

            for Secao in Secoes:
                if not os.path.exists("{0}\\{1}\\{2}\\o00{3}-{4}{5}{6}.logjez".format(downloaddir_root, UF, Municipio, cod_turno, cod_mun, Zona, Secao)):
                    downloadFiles(UF, Municipio, cod_mun, Zona, Secao, "{0}\\{1}\\{2}\\".format(downloaddir_root, UF, Municipio), cod_turno)
            
            progresso += 1
            print("Progresso: {0:.2f}%".format(progresso * 100 / progresso_total))