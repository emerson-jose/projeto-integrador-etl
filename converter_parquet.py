from pathlib import Path
import polars as pl
from funcoes import lento
def convertidos():
        caminho = Path("dados_analise")
        arq = list(caminho.glob("*.csv"))

        novo_caminho = Path("dados_convertidos_prt")
        novo_caminho.mkdir(exist_ok=True)

        # visualizando a quantidade de arquivos
        lento(f"Foram encontrados {len(arq)} arquivos na pasta dados_analise\n\n----listando arquivos para conversao----\n\n")

        # listando os nomes dos arquivos
        for arquivo in arq:
            lento(arquivo.stem)

        # convertendo CSVs para Parquet
        for arquivo in arq:
            df = pl.read_csv(arquivo, separator=",")
            
            # cria nome de parquet baseado no CSV
            novo_arquivo = novo_caminho / f"{arquivo.stem}.parquet"
            df.write_parquet(novo_arquivo)
            
        print(f"\nArquivos convertido com sucesso: [{novo_arquivo.absolute()}]")
        print("▭"*110)

        # listando arquivos convertidos
        print("\nArquivos no diretório dados_convertidos_prt\n ")
        for arquivo in novo_caminho.glob("*.parquet"):
            lento(arquivo.name)
        print("▭"*110)