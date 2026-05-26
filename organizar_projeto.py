import os
import shutil
from pathlib import Path

def organizar():
    # 1. Definir pastas
    pastas = ['backend', 'frontend']
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
        # Cria o __init__.py para transformar em módulo Python
        Path(f"{pasta}/__init__.py").touch()
        print(f"✔️ Pasta '{pasta}' preparada.")

    # 2. Mapeamento de arquivos
    backend_files = [
        'main.py', 
        'funcoes.py', 
        'extracao_dados_web.py', 
        'converter_parquet.py', 
        'tratando.py', 
        'conecao.py', 
        'inserir_dados.py'
    ]
    
    frontend_files = [
        'app_gui.py'
    ]

    # 3. Mover arquivos do Backend
    for arquivo in backend_files:
        if os.path.exists(arquivo):
            shutil.move(arquivo, f"backend/{arquivo}")
            print(f"➡️ {arquivo} movido para backend/")

    # 4. Mover arquivos do Frontend
    for arquivo in frontend_files:
        if os.path.exists(arquivo):
            shutil.move(arquivo, f"frontend/{arquivo}")
            print(f"➡️ {arquivo} movido para frontend/")

    print("\n🚀 Projeto reorganizado com sucesso!")
    print("Próximo passo: Atualize os imports conforme as instruções.")

if __name__ == "__main__":
    organizar()
