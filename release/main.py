import requests
import os

import network as Net
import data as Data
import bu as BU
import log as Log

#Net.downloadMunicipiosJSON()  #se nao tiver arquivo MunicipiosJSON.dat dentro da pasta data

Data.Estados = Net.loadMunicipiosJSON()

UF = "PI"

Net.downloadDatafromUF(UF)

#bu = BU.objBU(UF, "ACAUÃ", "0038", "0014")
#log = Log.objLog(UF, "ACAUÃ", "0038", "0014")

Data.criaArquivoCSV(UF, UF + ".csv")


#Funções úteis:
#   Net.downloadDatafromUF(UF)
#       download dos arquivos de urna de determinado estado para a pasta data:
#
#   Data.Estados = Net.loadMunicipiosJSON()
#       Necessário para carregar o arquivo MunicipiosJSON para poder executar as demais funções
#
#   Net.downloadMunicipiosJSON()
#       Faz download do arquivo MunicipiosJSON do portal TSE Resultados para a pasta data
#
#   Data.getCodeMunicipio(UF, municipio)
#       Retorna string numérica contendo código do município
#       Parâmetros:
#           UF -> string de 2 caracteres, exemplo: "PI"
#			municipio -> string do nome do municipio com acento em caixa alta, exemplo: "ACAUÃ"
#
#   bu = BU.objBU(UF, municipio, zona, secao)
#       Retorna um dicionario com todos os dados do arquivo BU
#       Parâmetros:
#           UF -> string de 2 caracteres, exemplo: "PI"
#			municipio -> string do nome do municipio com acento em caixa alta, exemplo: "ACAUÃ"
#			zona -> string contendo 4 caracteres numéricos, exemplo: "0038"
#           secao -> string contendo 4 caracteres numéricos, exemplo: "0001"
#       a classe objBU está no final do arquivo bu.py
#
#   Data.criaArquivoCSV(UF, filename)
#       Cria arquivo CSV a partir de arquivos BU dentro da pasta data