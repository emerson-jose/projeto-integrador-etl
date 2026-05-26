import time
from backend.extracao_dados_web import extracao
from backend.extracao_teste import extracao_playwright
from backend.converter_parquet import convertidos
from backend.tratando import tratados
from backend.conecao import testar_conexao
from backend.funcoes import lento

def executador():
    inicio_total = time.time()
    
    print("▭"*110)
    lento("             -------------------INICIANDO SEQUENCIA DE TAREFAS-------------------- 🐾\n")
    print("▭"*110)
    
    # 1. Extração Kaggle (API)
    inicio = time.time()
    lento("Iniciando Extração 1: Kaggle API...")
    extracao()
    tempo_extracao1 = time.time() - inicio
    
    time.sleep(1)
    
    # 2. Extração Playwright (Web)
    inicio = time.time()
    lento("Iniciando Extração 2: Playwright Web...")
    extracao_playwright()
    tempo_extracao2 = time.time() - inicio
    
    time.sleep(1)
    
    # 3. Conversão
    inicio = time.time()
    convertidos()
    tempo_conversao = time.time() - inicio
    
    time.sleep(1)
    
    # 4. Tratamento
    inicio = time.time()
    tratados()
    tempo_tratamento = time.time() - inicio
    
    time.sleep(1)
    
    # 5. Conexão e Carga (DIRETO PARA SUPABASE)
    inicio = time.time()
    from backend.inserir_dados import inserir_no_banco
    inserir_no_banco()
    tempo_conexao = time.time() - inicio
    
    fim_total = time.time()
    tempo_total = fim_total - inicio_total
    
    # Resumo Final
    print("\n" + "▭"*110)
    lento("             ------------------- RESUMO DE EXECUÇÃO CLOUD-NATIVE -------------------- ☁️")
    print("▭"*110)
    lento(f"⏱️ Tempo de Extração (Fontes Externas): {tempo_extracao1 + tempo_extracao2:.2f}s")
    lento(f"⏱️ Tempo de Conversão/Tratamento: {tempo_conversao + tempo_tratamento:.2f}s")
    lento(f"⏱️ Tempo de Carga Direta Supabase: {tempo_conexao:.2f}s")
    print("-" * 30)
    lento(f"🚀 TOTAL CLOUD PIPELINE: {tempo_total:.2f} segundos")
    print("▭"*110)

if __name__ == "__main__":
    executador()

