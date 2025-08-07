from datetime import datetime
import pandas as pd
import os
import glob

def modificaCsv(grupo, filial):
    #setando caminho para as pastas 
    pasta_xls = 'documentos\csv'
    pasta_csv = 'documentos\xls'

    #grupo = 16
    #filial = 1008053

    agora = datetime.now()
    mes = agora.month
    ano = agora.year

    # Busca todos os arquivos .XLS na pasta
    arquivos_xls = glob.glob(os.path.join(pasta_xls, '*.xls'))

    for arquivo_xls in arquivos_xls:
        nome_arquivo = os.path.basename(arquivo_xls)
        
        # Ler o arquivo .xls usando o caminho completo
        df = pd.read_excel(nome_arquivo)
        
        # Criar nome para o CSV com dados da variável e nome do arquivo original (opcional)
        arquivo_csv = (f"NFe{grupo}_{filial}_{mes}{ano}.csv")

        caminho_csv = os.path.join(pasta_csv, arquivo_csv)
        
        # Salvar como .csv
        df.to_csv(caminho_csv, index=False)
        
        print(f"Arquivo convertido e salvo como {arquivo_csv}")
