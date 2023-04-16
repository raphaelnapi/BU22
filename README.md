# BU22
Script em Python para download e análise de dados de boletim de urna do 1º e 2º turno das eleições 2022

# Requisitos
Para executar o script é necessário instalar os seguintes módulos: requests, asn1 e py7zr.

Para isso, utilize os seguintes comandos no Prompt de Comando:
```bash
python -m install pip requests
python -m install pip asn1
python -m install pip py7zr
```

# Utilização do BU22

```Python
Data.Estados = Data.loadMunicipiosJSON() #utilizado para carregar dados de todos os municipios do Brasil
Net.downloadDataFromUF("PI", 2) #Faz download de dados do 2º turno das urnas do PIAUÍ
Data.criaArquivosCSV("PI", 2) #Lê os arquivos BU e LOG do 2º turno do PIAUÍ e registra os dados em um arquivo CSV
```

## Funções úteis

Download do arquivo MunicipiosJSON do portal TSE Resultados para a pasta data:
```Python
Net.downloadMunicipiosJSON()
```

Carrega o arquivo MunicipiosJSON:
```Python
   Data.Estados = Net.loadMunicipiosJSON()
   ```

Download dos arquivos de urna de determinado estado e turno para a pasta data\download:
```Python
Net.downloadDatafromUF("MG", 1)
```

Retorna string com o código do município:
```Python
Data.getCodeMunicipio("PI", "ACAUÃ")
```

Retorna dicionário com todos os dados do arquivo BU de determinada seção no 1º ou 2º turno:
```Python
bu = BU.objBU("PI", "ACAUÃ", "0038", "0001", 1)
```

Cria arquivo CSV de determinado estado a partir de arquivos *.BU e *.LOG dentro da pasta data:
```Python
Data.criaArquivosCSV("MG", 1)
```
