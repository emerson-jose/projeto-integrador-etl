import os
from datetime import datetime
from playwright.sync_api import sync_playwright
import time
from backend.funcoes import lento

def extracao_playwright():
    instante = datetime.now()
    pasta_destino = 'dados_analise'

    # Cria a pasta caso ela ainda não exista
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        print("▭"*110)
        lento(f"------------status ✅ SUCESSO!------------\nA pasta '{pasta_destino}' criada com sucesso! 📁\n em {instante.day}/{instante.month}/{instante.year}")
    else:
        lento(f"status: A pasta '{pasta_destino}' já existe. Vamos salvar os arquivos nela. 📁")
        print("▭"*110)

    lento("Preparando para baixar os dados via Playwright...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            page.goto("https://mavenanalytics.io/data-playground/crm-sales-opportunities")
            
            lento("Iniciando o download do dataset...")
            with page.expect_download() as download_info:
                # O seletor pode precisar de ajuste dependendo da página
                page.get_by_role("link", name="Download dataset").click()
            
            download = download_info.value
            nome_original = download.suggested_filename
            nome_base, extensao = os.path.splitext(nome_original)
            novo_nome = f"{nome_base}_maven{extensao}"
            caminho_arquivo = os.path.join(pasta_destino, novo_nome)
            download.save_as(caminho_arquivo)
            
            lento(f"✅ Download concluído: {novo_nome}")
            
            # Unzip if it's a zip file
            if novo_nome.endswith('.zip'):
                lento("Extraindo arquivos...")
                import zipfile
                with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
                    # Ao extrair, precisamos garantir que os arquivos extraídos também não sobrescrevam
                    # Mas o Maven zip geralmente contém os mesmos nomes de arquivos CSV.
                    # Vamos extrair para uma subpasta temporária e renomear.
                    temp_extract = os.path.join(pasta_destino, "temp_maven")
                    zip_ref.extractall(temp_extract)
                    
                    for arq_extraido in os.listdir(temp_extract):
                        if arq_extraido.endswith('.csv'):
                            nome_e, ext_e = os.path.splitext(arq_extraido)
                            os.rename(
                                os.path.join(temp_extract, arq_extraido),
                                os.path.join(pasta_destino, f"{nome_e}_maven{ext_e}")
                            )
                    # Limpeza
                    import shutil
                    shutil.rmtree(temp_extract)
                os.remove(caminho_arquivo)
                lento(f"✅ SUCESSO! Os arquivos foram extraídos e renomeados em: {pasta_destino}")
            else:
                lento(f"✅ SUCESSO! O arquivo foi salvo como: {novo_nome}")
            
            print("▭"*110)
            
        except Exception as e:
            lento(f"❌ status: Erro durante a extração Playwright: {e}")
        finally:
            time.sleep(2) # Pequena espera para garantir finalização
            browser.close()

if __name__ == "__main__":
    extracao_playwright()