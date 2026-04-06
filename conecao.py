import mysql.connector
from mysql.connector import Error
from inserir_dados import inserir_no_banco

def testar_conexao():
    print("---------------TESTE DE CONECAO COM O BANCO ---------------")
    try:
        # 1. Tenta estabelecer a conexão (Substitua pelas suas credenciais)
        conexao = mysql.connector.connect(
            host='localhost',        # Geralmente 'localhost' ou '127.0.0.1'
            user='root',      # Geralmente 'root'
            password='4321',    # A senha que você usa no Workbench
            database='crm_vendas'    # O nome do banco que criamos
        )

        # 2. Verifica se a conexão foi bem sucedida
        if conexao.is_connected():
            info_servidor = conexao.get_server_info()
            print(f"✅ Conectado com sucesso ao Servidor MySQL (Versão {info_servidor})")
            
            # 3. Executa um comando simples para confirmar o banco de dados ativo
            cursor = conexao.cursor()
            cursor.execute("SELECT database();")
            linha = cursor.fetchone()
            print(f"✅ Banco de dados atual: {linha[0]}")

    except Error as erro:
        # Se algo der errado (senha incorreta, servidor desligado, etc.), avisa aqui
        print(f"❌ Erro ao tentar conectar ao MySQL:\n{erro}")
        
        
        # ==========================================
        # LÓGICA PRINCIPAL (O GATILHO)
        # ==========================================
    finally:
        # 4. Garante que a conexão será fechada após o teste, evitando travar o banco
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
            print("🔌 Conexão encerrada com segurança.")
            inserir_no_banco()

# Executa o teste