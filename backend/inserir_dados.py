import polars as pl
import pandas as pd
import time
from pathlib import Path
from backend.funcoes import lento
from backend.conecao_supar import get_engine, testar_conexao_supabase

def inserir_no_banco():
    """
    Novo processo de carga: Lê arquivos Parquet tratados e insere DIRETAMENTE no Supabase.
    Substitui a antiga carga para o MariaDB.
    """
    if not testar_conexao_supabase():
        lento("❌ Cancelando carga: Falha de conexão com a Nuvem.")
        return

    engine = get_engine()
    diretorio_tratados = Path("arquivos_tratados")

    # Mapeamento Global (Origem Parquet -> Destino Supabase)
    config_carga = {
        "accounts.parquet": {
            "tabela": "stg_contas",
            "renomear": {
                "ano_fundacao": "ano_estabelecimento",
                "receita": "receita_anual",
                "funcionarios": "empregados",
                "subsidiaria_de": "matriz"
            }
        },
        "sales_teams.parquet": {
            "tabela": "stg_vendedores",
            "renomear": {"agente_vendas": "vendedor"}
        },
        "products.parquet": {
            "tabela": "stg_produtos",
            "renomear": {
                "serie": "series",
                "preco_venda": "preco_minimo_venda"
            }
        },
        "sales_pipeline.parquet": {
            "tabela": "stg_funil_vendas",
            "renomear": {
                "id_oportunidade": "id_proposta",
                "agente_vendas": "vendedor",
                "fase_negociacao": "status_negocio",
                "data_engajamento": "data_proposta",
                "data_fechamento": "data_encerramento",
                "valor_fechamento": "valor_acordado"
            }
        }
    }

    try:
        for arquivo_nome, config in config_carga.items():
            caminho = diretorio_tratados / arquivo_nome
            
            if caminho.exists():
                lento(f"⏳ Processando '{arquivo_nome}' para Nuvem...")
                
                # Usamos Polars para leitura veloz e Pandas para inserção compatível com SQLAlchemy
                df = pl.read_parquet(caminho).to_pandas()
                
                # Aplica Renomeação conforme Requisito
                df = df.rename(columns=config["renomear"])
                
                # Conversão para Texto (Padronização Staging Supabase)
                df = df.astype(str).replace('nan', '')

                # Carga Direta no Supabase
                df.to_sql(
                    config["tabela"], 
                    engine, 
                    if_exists='append', 
                    index=False, 
                    method='multi'
                )
                
                lento(f"✅ Sucesso: {len(df)} linhas enviadas para '{config['tabela']}'.")
            else:
                lento(f"⚠️ Arquivo '{arquivo_nome}' não encontrado localmente.")

        lento(f"\n✨ [{time.strftime('%H:%M:%S')}] CARGA CLOUD CONCLUÍDA!")

    except Exception as e:
        lento(f"❌ Erro durante a carga no Supabase: {e}")

if __name__ == "__main__":
    inserir_no_banco()
