import pandas as pd
import warnings
import time
from sqlalchemy import text
from backend.conecao_supar import get_engine
from typing import Dict, Any

warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

class DBManager:
    """Gerenciador de dados otimizado para Cloud (Client-Side Joining)."""
    
    def __init__(self):
        self.engine = get_engine()

    def get_dados_completos(self, agente: str = "Todos", periodo: str = "Todos") -> pd.DataFrame:
        """
        Busca as tabelas separadamente e realiza o Join no Pandas para evitar lentidão no SQL Cloud.
        """
        start_time = time.time()
        print(f"🔍 [DB] Iniciando extração otimizada da Nuvem...")

        try:
            with self.engine.connect() as conn:
                # 1. Baixar Tabela Principal (Funil)
                print("📡 [DB] Baixando Funil de Vendas...")
                df_funil = pd.read_sql(text("SELECT * FROM stg_funil_vendas"), conn)
                
                # 2. Baixar Tabelas de Apoio (Dimensões)
                print("📡 [DB] Baixando Tabelas de Apoio (Vendedores, Contas, Produtos)...")
                df_vend = pd.read_sql(text("SELECT * FROM stg_vendedores"), conn)
                df_cont = pd.read_sql(text("SELECT * FROM stg_contas"), conn)
                df_prod = pd.read_sql(text("SELECT * FROM stg_produtos"), conn)

            # Limpeza de strings para evitar falhas no Merge
            for d in [df_funil, df_vend, df_cont, df_prod]:
                for col in d.columns:
                    if d[col].dtype == 'object':
                        d[col] = d[col].str.strip()

            print(f"⚙️ [DB] Cruzando dados localmente ({len(df_funil)} registros)...")
            
            # Realizar os Joins no Pandas
            df = df_funil.merge(df_vend, on="vendedor", how="left")
            df = df.merge(df_cont, on="conta", how="left")
            df = df.merge(df_prod, on="produto", how="left")

            # Tratamento de tipos
            df['valor_acordado'] = pd.to_numeric(df['valor_acordado'], errors='coerce').fillna(0.0)
            df['data_encerramento'] = pd.to_datetime(df['data_encerramento'], errors='coerce')
            df['data_proposta'] = pd.to_datetime(df['data_proposta'], errors='coerce')

            # Filtros em memória
            if agente != "Todos":
                df = df[df['vendedor'] == agente]
            
            if periodo != "Todos":
                referencia = df['data_encerramento'].max()
                if pd.isna(referencia): referencia = pd.Timestamp.now()

                if periodo == "Último Mês":
                    inicio = referencia - pd.DateOffset(months=1)
                    df = df[df['data_encerramento'] >= inicio]
                elif periodo == "Último Trimestre":
                    inicio = referencia - pd.DateOffset(months=3)
                    df = df[df['data_encerramento'] >= inicio]
                elif periodo == "Este Ano":
                    df = df[df['data_encerramento'].dt.year == referencia.year]

            end_time = time.time()
            print(f"✅ [DB] Operação concluída em {end_time - start_time:.2f}s!")
            return df
            
        except Exception as e:
            print(f"❌ [DB] Erro na extração: {e}")
            return pd.DataFrame()

    def atualizar_oportunidade(self, id_proposta: str, novos_dados: Dict[str, Any]) -> bool:
        """Atualiza um registro diretamente na nuvem."""
        if not novos_dados: return False
        campos = ", ".join([f"{k} = :{k}" for k in novos_dados.keys()])
        query = text(f"UPDATE stg_funil_vendas SET {campos} WHERE id_proposta = :id_proposta")
        novos_dados['id_proposta'] = id_proposta
        try:
            with self.engine.begin() as conn:
                result = conn.execute(query, novos_dados)
                return result.rowcount > 0
        except Exception as e:
            print(f"❌ Erro ao atualizar Supabase: {e}")
            return False
