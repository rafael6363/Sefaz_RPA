import os
import pandas as pd
usuario = os.getlogin()
caminho = 'downloads/xls'

def ultimoArquivoDownloads():
    # Atualiza a lista de arquivos a cada chamada
    lista = os.listdir(caminho)
    lis_dat = []
    for arquivo in lista:
        caminho_arquivo = fr"{caminho}/{arquivo}"
        if os.path.isfile(caminho_arquivo):  # Garante que é arquivo
            data = os.path.getmtime(caminho_arquivo)
            lis_dat.append((data, arquivo))

    # Verifica se encontrou arquivos
    if not lis_dat:
        print("Nenhum arquivo encontrado.")
        return None

    # Ordena e retorna o mais recente
    lis_dat.sort(reverse=True)
    ult_arq = lis_dat[0]
    print(f"Último arquivo: {ult_arq}")
    return ult_arq

def coverterExcelpCsv(consulta,grupo,filial):
    ultimoArq  =  ultimoArquivoDownloads()
    #le o excel e converte em csv
    read = pd.read_excel(fr"{caminho}\{ultimoArq[1]}")
    read.to_csv(f"sequencianotas\csv\Consulta.csv", index=False)
    #le as linhas do csv
    df = pd.read_csv(f"sequencianotas\csv\Consulta.csv",index_col=None)

    # Exclui as 5 primeiras linhas
    df = df.iloc[5:]
    df.replace(' " ', "")
    print('tira as primeiras 5 linhas do csv')
    # Salva o DataFrame modificado em um novo arquivo CSV
    df.to_csv(fr"sequencianotas\csv\Consulta.csv", header=False, index=False, sep=';')
    #remove o ultimo download feito deixando somente o csv 
    os.remove(fr"{caminho}\{ultimoArq[1]}")
    print("removido o ultimo arquivo do downloads")

if __name__ == "__main__":
    coverterExcelpCsv()    