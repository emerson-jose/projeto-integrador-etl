import polars as pl
import mysql.connector
from mysql.connector import Error
from pathlib import Path
from funcoes import lento

def testar_conexao():
    lento("--------------- TESTE DE CONEXÃO COM O BANCO ---------------")
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='4321',
            database='crm_vendas'
        )

        if conexao.is_connected():
            info_servidor = conexao.get_server_info()
            lento(f"✅ Conectado com sucesso ao Servidor MySQL (Versão {info_servidor})")
            
            cursor = conexao.cursor()
            cursor.execute("SELECT database();")
            linha = cursor.fetchone()
            lento(f"✅ Banco de dados atual: {linha[0]}")
            
            return True  # Gatilho de sucesso

    except Error as erro:
        print(f"❌ Erro ao tentar conectar ao MySQL:\n{erro}")
        return False # Gatilho de falha
        
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
            lento("🔌 Conexão de teste encerrada.\n")


def inserir_no_banco():
    # 1. Configuração da Conexão
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',      # <-- Seu usuário real
            password='4321',  # <-- Sua senha real
            database='crm_vendas'
        )
        cursor = conexao.cursor()
        lento("✅ Conectado ao banco de dados crm_vendas.")

    except Error as e:
        print(f"❌ Erro ao conectar: {e}")
        return

    # 2. Pasta onde estão os arquivos tratados
    diretorio_tratados = Path("arquivos_tratados")

    # 3. Mapeamento dos arquivos, tabelas e queries de inserção
    # AJUSTE: Adicionado 'INSERT IGNORE' em todas as queries!
    operacoes = [
        {
            "arquivo": "metadata.parquet",
            "tabela": "metadados",
            "query": "INSERT IGNORE INTO metadados (tabela, campo, descricao) VALUES (%s, %s, %s)"
        },
        {
            "arquivo": "products.parquet",
            "tabela": "produtos",
            "query": "INSERT IGNORE INTO produtos (produto, serie, preco_venda) VALUES (%s, %s, %s)"
        },
        {
            "arquivo": "sales_teams.parquet",
            "tabela": "equipes_vendas",
            "query": "INSERT IGNORE INTO equipes_vendas (agente_vendas, gerente, escritorio_regional) VALUES (%s, %s, %s)"
        },
        {
            "arquivo": "accounts.parquet",
            "tabela": "contas",
            "query": "INSERT IGNORE INTO contas (conta, setor, ano_fundacao, receita, funcionarios, local_escritorio, subsidiaria_de) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        },
        {
            "arquivo": "sales_pipeline.parquet",
            "tabela": "pipeline_vendas",
            "query": "INSERT IGNORE INTO pipeline_vendas (id_oportunidade, agente_vendas, produto, conta, fase_negociacao, data_engajamento, data_fechamento, valor_fechamento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        }
    ]

    # 4. Loop de Inserção
    try:
        for op in operacoes:
            caminho = diretorio_tratados / op["arquivo"]
            
            if caminho.exists():
                lento(f"⏳ Inserindo dados na tabela '{op['tabela']}'...")
                
                # Lê o parquet com o Polars
                df = pl.read_parquet(caminho)
                
                # Converte o DataFrame do Polars para uma lista de tuplas
                dados = df.rows()
                
                # Executa a query para todas as linhas de uma vez
                cursor.executemany(op["query"], dados)
                
                # Salva as alterações no banco (Commit)
                conexao.commit()
                # Aqui o rowcount vai mostrar 0 para quem já foi inserido, e os números novos para as linhas do pipeline!
                lento(f"   ✔️ {cursor.rowcount} linhas inseridas com sucesso!")
            else:
                print(f"⚠️ Arquivo {op['arquivo']} não encontrado. Pulando...")

        lento("\n🚀 Carga de dados concluída com sucesso!")

    except Error as e:
        print(f"❌ Erro durante a inserção: {e}")
        conexao.rollback() # Desfaz as alterações caso dê erro

    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
            lento("🔌 Conexão encerrada com sucesso.")


# ==========================================
# LÓGICA PRINCIPAL (O GATILHO)
# ==========================================
