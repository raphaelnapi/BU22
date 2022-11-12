# BU22
Download e análise de dados de boletim de urna do 1º e 2º turno das eleições 2022

Para executar o script é necessário instalar os seguintes módulos: requests, asn1 e py7zr.

Utilize os comandos:
python -m install pip requests
python -m install pip asn1
python -m install pip py7zr

Exemplo simples de utilização do script:
Data.Estados = Data.loadMunicipiosJSON() #utilizado para carregar dados de todos os municipios do Brasil
Net.downloadDataFromUF("PI", 2) #download de dados de urnas do 2º turno do PIAUÍ
Data.criaArquivosCSV("PI", 2) #compila os dados em arquivo CSV

#Funções úteis:
#   Data.Estados = Net.loadMunicipiosJSON()
#       Necessário para carregar o arquivo MunicipiosJSON para poder executar as demais funções
#
#   Net.downloadDatafromUF("MG", 1)
#       download dos arquivos de urna de determinado estado e turno para a pasta data\download
#       Para baixar dados do segundo turno troque 1 por 2
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
#   bu = BU.objBU(UF, municipio, zona, secao, turno)
#       Retorna um dicionario com todos os dados do arquivo BU
#       Parâmetros:
#           UF -> string de 2 caracteres, exemplo: "PI"
#			municipio -> string do nome do municipio com acento em caixa alta, exemplo: "ACAUÃ"
#			zona -> string contendo 4 caracteres numéricos, exemplo: "0038"
#           secao -> string contendo 4 caracteres numéricos, exemplo: "0001"
#           turno -> int (1 ou 2)
#       a classe objBU está no final do arquivo bu.py
#
#   Data.criaArquivosCSV("MG", 1)
#       Cria arquivo CSV a partir de arquivos BU dentro da pasta data
#       Para manipular dados do segundo turno troque 1 por 2
