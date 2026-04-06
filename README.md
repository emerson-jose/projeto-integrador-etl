# Pipeline de Dados ETL - CRM de Vendas (Projeto Integrador)

Este projeto é um pipeline completo de Extração, Transformação e Carga (ETL) construído em Python. Ele automatiza o fluxo de dados desde a extração na web, conversão de formatos, tratamento de dados brutos (limpeza e normalização) até a inserção em um banco de dados relacional MySQL para futuras análises.

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Polars:** Processamento e transformação de dados em altíssima velocidade.
* **MySQL / MariaDB:** Banco de dados relacional (SGBD).
* **mysql-connector-python:** Comunicação e integração entre o Python e o banco de dados.
* **Pathlib:** Manipulação moderna e segura de diretórios.

## 📁 Estrutura do Projeto e Arquitetura

O projeto foi modularizado para separar as responsabilidades de cada etapa do pipeline:

### 📂 Diretórios
* `dados_convertidos_prt/`: Recebe os arquivos convertidos para o formato `.parquet` (Dados Brutos).
* `arquivos_tratados/`: Recebe os arquivos após a limpeza e normalização (Dados Prontos para Carga).
* `dados_analise/`: Diretório destinado ao armazenamento de visões, relatórios ou exportações analíticas geradas após a carga.

### 🐍 Scripts Python
* **`extracao_dados_web.py`**: Responsável por extrair os dados da fonte original (Web Scraping / API). *(Etapa: Extract)*
* **`converter_parquet.py`**: Converte os dados brutos extraídos para o formato colunar `.parquet`, otimizando a leitura.
* **`tratando.py`**: Aplica as regras de negócio, renomeia colunas, formata datas e valores monetários, e trata dados nulos usando Polars. *(Etapa: Transform)*
* **`conecao.py`**: Módulo responsável por gerenciar e testar a conexão com o banco de dados MySQL.
* **`inserir_dados.py`**: Lê os arquivos tratados e realiza a carga no banco de dados respeitando a ordem das chaves estrangeiras e usando `INSERT IGNORE` para evitar duplicidades. *(Etapa: Load)*
* **`funcoes.py`**: Módulo de utilidades do sistema (contém funções de apoio visual, como impressões no terminal).
* **`main.py`**: O orquestrador principal do projeto. Pode ser utilizado para executar todo o pipeline (ETL) em sequência com um único comando.

## ⚙️ Pré-requisitos e Configuração

1. Ter o banco de dados MySQL ou MariaDB rodando localmente (`localhost`).
2. Criar a estrutura do banco de dados relacional executando as queries SQL (Tabelas: `metadados`, `produtos`, `equipes_vendas`, `contas`, `pipeline_vendas`).
3. Instalar as dependências do Python:
   ```bash
   pip install polars mysql-connector-python