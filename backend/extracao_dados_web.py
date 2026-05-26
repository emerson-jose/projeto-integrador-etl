def extracao():
    import os
    from datetime import datetime
    import time 
    from backend.funcoes import lento
     
    # 1. CREDENCIAIS DO KAGGLE (Carregadas do .env para segurança)
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv('KAGGLE_API_TOKEN')
    if token:
        os.environ['KAGGLE_API_TOKEN'] = token
    else:
        lento("⚠️ Aviso: KAGGLE_API_TOKEN não encontrado no ambiente.")

    #importamos o Kaggle
    import kaggle 
    # usamos para poder fazer um tipo de status pelo horario 
    instante = datetime.now()

    lento("Preparando para baixar os dados...")
    
    try:
        # 2. Definimos qual dataset queremos baixar
        nome_dataset = 'agungpambudi/crm-sales-predictive-analytics'
        
        # 3. Definimos o nome da pasta
        pasta_destino = 'dados_analise'
        
        # Cria a pasta caso ela ainda não exista
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
            print("▭"*110)
            lento(f"------------status ✅ SUCESSO!------------\nA pasta '{pasta_destino}' criada com sucesso! 📁\n em {instante.day}/{instante.month}/{instante.year}")
        else:
            lento(f"status: A pasta '{pasta_destino}' já existe. Limpando arquivos antigos... 📁")
            # Tenta remover arquivos antigos para evitar erro de permissão ao sobrescrever
            for arquivo in os.listdir(pasta_destino):
                if arquivo.endswith(".csv"):
                    try:
                        os.remove(os.path.join(pasta_destino, arquivo))
                    except Exception:
                        pass # Se não conseguir, o kaggle tentará sobrescrever depois
            print("▭"*110)
        lento(f"Conectando ao Kaggle e baixando o arquivo... isso pode levar alguns segundos ⌛")
        print("▭"*110)
        
        # 4. Baixa e extrai os arquivos (unzip=True)
        kaggle.api.dataset_download_files(nome_dataset, path=pasta_destino, unzip=True)
        lento(f"status: ✅ SUCESSO! O download foi concluído e os arquivos estão descompactados na pasta '{pasta_destino}'! 🚀")
        print("▭"*110)
    except Exception as e:
        lento(f"❌ status: Ops, ocorreu um erro durante o download: {e}")
