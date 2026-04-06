
import time
from extracao_dados_web import extracao
from converter_parquet import convertidos
from datetime import datetime
from tratando import tratados
from conecao import testar_conexao
    
def executador():
    print("▭"*110)
    print("          -------------------INICIANDO SEQUENCIA DE TAREFAS-------------------- 🐾\n")
    print("▭"*110)
    
    time.sleep(3)
    extracao()
    
    time.sleep(3)
    convertidos()
    
    time.sleep(3)
    tratados()
    
    time.sleep(3)
    testar_conexao()   
executador()

