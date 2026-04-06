import polars as pl
from pathlib import Path
from funcoes import lento

def tratados():
    
    print("-----------tratando dados para fazer a conecaocom o banco de dados---------\n")
    # 1. Definir os diretórios de origem e destino (Caminhos relativos)
    diretorio_origem = Path("dados_convertidos_prt")
    diretorio_destino = Path("arquivos_tratados")
    
    # Criar a pasta de destino caso ela não exista
    diretorio_destino.mkdir(exist_ok=True)

    # 2. Dicionário de mapeamento completo para renomear as colunas
    mapeamento_colunas = {
        "sales_pipeline.parquet": {
            "opportunity_id": "id_oportunidade",
            "sales_agent": "agente_vendas",
            "product": "produto",
            "account": "conta",
            "deal_stage": "fase_negociacao",
            "engage_date": "data_engajamento",
            "close_date": "data_fechamento",
            "close_value": "valor_fechamento"
        },
        "sales_teams.parquet": {
            "sales_agent": "agente_vendas",
            "manager": "gerente",
            "regional_office": "escritorio_regional"
        },
        "products.parquet": {
            "product": "produto",
            "series": "serie",
            "sales_price": "preco_venda"
        },
        "accounts.parquet": {
            "account": "conta",
            "sector": "setor",
            "year_established": "ano_fundacao",
            "revenue": "receita",
            "employees": "funcionarios",
            "office_location": "local_escritorio",
            "subsidiary_of": "subsidiaria_de"
        },
        "metadata.parquet": {
            "Table": "tabela",
            "Field": "campo",
            "Description": "descricao"
        }
    }

    # 3. Iterar sobre todos os arquivos .parquet da pasta origem
    for caminho_arquivo in diretorio_origem.glob("*.parquet"):
        nome_arquivo = caminho_arquivo.name
        lento(f"Processando: {nome_arquivo}...")

        # Ler o arquivo parquet
        df = pl.read_parquet(caminho_arquivo)

        # --- ETAPA A: RENOMEAR COLUNAS ---
        if nome_arquivo in mapeamento_colunas and mapeamento_colunas[nome_arquivo]:
            colunas_para_renomear = {
                k: v for k, v in mapeamento_colunas[nome_arquivo].items() if k in df.columns
            }
            df = df.rename(colunas_para_renomear)

        # --- ETAPA B: TRATAMENTO PARA O BANCO DE DADOS (MYSQL) ---
        # Mantém nulos autênticos e formata datas/dinheiro corretamente
        if nome_arquivo == "sales_pipeline.parquet":
            df = df.with_columns([
                pl.col("data_engajamento").str.strptime(pl.Date, "%Y-%m-%d", strict=False),
                pl.col("data_fechamento").str.strptime(pl.Date, "%Y-%m-%d", strict=False),
                pl.col("valor_fechamento").cast(pl.Float64)
            ])
            
        elif nome_arquivo == "products.parquet":
            df = df.with_columns(pl.col("preco_venda").cast(pl.Float64))
            
        elif nome_arquivo == "accounts.parquet":
             df = df.with_columns(pl.col("receita").cast(pl.Float64))

        # --- ETAPA C: SALVAR NO NOVO DIRETÓRIO ---
        caminho_salvar = diretorio_destino / nome_arquivo
        df.write_parquet(caminho_salvar)

    lento("\n🚀 Todos os arquivos foram tratados para o MySQL e salvos com sucesso!")

