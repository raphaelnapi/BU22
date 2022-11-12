import requests
import os

import network as Net
import data as Data
import bu as BU
import log as Log
import const

Data.Estados = Data.loadMunicipiosJSON()
Net.downloadDatafromUF("PI", 2) #download de dados do 2º Turno do PIAUÍ
Data.criaArquivosCSV("PI", 2) #extrai dados de arquivos do 2º Turno/PIAUÍ e organiza em arquivo CSV


#Funções úteis:
#   Data.Estados = Net.loadMunicipiosJSON()
#       Necessário para carregar o arquivo MunicipiosJSON para poder executar as demais funções
#
#   Net.downloadDatafromUF("MG", 1)
#       download dos arquivos de urnas do primeiro turno de determinado estado para a pasta data\Downloads.
#       Para baixar dados do segundo turno substitua 1 por 2
#
#   Net.downloadMunicipiosJSON()
#       Faz download do arquivo MunicipiosJSON do portal TSE Resultados para a pasta data
#       Caso nao tenha o arquivo MunicipiosJSON.dat na pasta data. Necessário para Data.Estados = Data.loadMunicipiosJSON()
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
#   Data.criaArquivosCSV("MG", 1)
#       Cria arquivo CSV a partir de arquivos BU dentro da pasta data\Downloads
#       Substitua 1 por 2 se forem dados do segundo turno