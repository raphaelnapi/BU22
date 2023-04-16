# BU22
Script em Python para download e análise de dados de boletim de urna do 1º e 2º turno das eleições 2022

# Requisitos
Para executar o script é necessário instalar os seguintes módulos: requests, asn1 e py7zr.

Para isso, utilize os seguintes comandos no terminal do VS Code:
```bash
pip install requests
pip install asn1
pip install py7zr
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

# Banco de Dados
Para correto funcionamento das funções de análise dos arquivos BU e LOG estes arquivos devem estar organizados da seguinte forma:
```
- Pasta nomeada com UF
- - Pasta nomeada com município em caixa alta
- - - Arquivos BU e Log
```

Exemplo:
```
- RJ
- - ANGRA DOS REIS
- - - o00406-5801701160001.bu
- - - o00406-5801701160001.logjez
- - - o00406-5801701160001.rdv
- - - o00406-5801701160002.bu
- - - ...
```
