def extracao():
    import os
    from datetime import datetime
    import time 
    
    def text_lento(texto):
        for letra in texto:
            print(letra, end ='',flush=True)
            time.sleep(0.03)
        print()
        
       
    
    # 1. CREDENCIAIS DO KAGGLE
    os.environ['KAGGLE_API_TOKEN'] = 'KGAT_f24013a07d89794c36d117cb7b6d67db' 

    #importamos o Kaggle
    import kaggle 
    
    # usamos para poder fazer um tipo de status pelo horario 
    instante = datetime.now()

    text_lento("Preparando para baixar os dados...")
    
    
    try:
        # 2. Definimos qual dataset queremos baixar
        nome_dataset = 'agungpambudi/crm-sales-predictive-analytics'
        
        # 3. Definimos o nome da pasta
        pasta_destino = 'dados_analise'
        
        # Cria a pasta caso ela ainda não exista
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
            print("▭"*110)
            text_lento(f"------------status ✅ SUCESSO!------------\nA pasta '{pasta_destino}' criada com sucesso! 📁\n em {instante.day}/{instante.month}/{instante.year}\n as {instante.hour:02}:{instante.minute:02}")
        else:
            text_lento(f"status: {instante.hour:02}:{instante.minute:02} A pasta '{pasta_destino}' já existe. Vamos salvar os arquivos nela. 📁")
            print("▭"*110)
        text_lento(f"Conectando ao Kaggle e baixando o arquivo... isso pode levar alguns segundos ⌛")
        print("▭"*110)
        
        # 4. Baixa e extrai os arquivos (unzip=True)
        kaggle.api.dataset_download_files(nome_dataset, path=pasta_destino, unzip=True)
        text_lento(f"status: {instante.hour:02}:{instante.minute:02} ✅ SUCESSO! O download foi concluído e os arquivos estão descompactados na pasta '{pasta_destino}'! 🚀")
        print("▭"*110)
    except Exception as e:
        text_lento(f"❌ status:{instante.hour:02}:{instante.minute:02} Ops, ocorreu um erro durante o download: {e}")
