import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from backend.funcoes import lento

from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Configurações de Conexão (Preferencialmente via variáveis de ambiente)
DB_HOST = os.getenv("SUPABASE_DB_HOST", "db.oqezzrwschncojmxkfts.supabase.co")
DB_PORT = os.getenv("SUPABASE_DB_PORT", "6543")
DB_NAME = os.getenv("SUPABASE_DB_NAME", "postgres")
DB_USER = os.getenv("SUPABASE_DB_USER", "postgres")
DB_PASSWORD = os.getenv("SUPABASE_DB_PASSWORD") 

if not DB_PASSWORD:
    # Fallback apenas para desenvolvimento local (CUIDADO ao subir para o GitHub)
    DB_PASSWORD = "BD#Ie$b2026"

# URL de conexão com SSL obrigatório para Supabase
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"

# Singleton para evitar múltiplas criações de engine
_engine = None

def get_engine():
    """Retorna a engine global com configurações de timeout e pool."""
    global _engine
    if _engine is None:
        _engine = create_engine(
            DATABASE_URL, 
            pool_pre_ping=True,
            connect_args={"connect_timeout": 10} # Desiste após 10s se não conectar
        )
    return _engine

def testar_conexao_supabase():
    """Testa a conectividade com o Supabase e retorna True se OK."""
    lento(f"⏳ [{time.strftime('%H:%M:%S')}] Validando conexão com Data Warehouse (Supabase)...")
    try:
        engine = get_engine()
        with engine.connect() as conexao:
            conexao.execute(text("SELECT 1"))
            lento(f"✅ [{time.strftime('%H:%M:%S')}] Conexão Cloud estabelecida com sucesso!")
            return True
    except SQLAlchemyError as e:
        lento(f"❌ [{time.strftime('%H:%M:%S')}] Falha na conexão Cloud: {e}")
        return False

def iniciar_fluxo_supabase():
    """Antigo ponto de entrada, mantido para compatibilidade inicial, agora apenas valida."""
    return testar_conexao_supabase()

if __name__ == "__main__":
    # Teste isolado do módulo
    iniciar_fluxo_supabase()
