import os
import shutil

# Caminho base
base_path = r'C:\SPED_fiscal'

# Estrutura de diretórios que você quer garantir
tipos = [
    'Consulta de CT-e Emitida\\Recebida',
    'Consulta de NF-e Emitida\\Recebida'
]

# Cria 12 meses para cada tipo de consulta
for tipo in tipos:
    for mes in range(1, 13):
        nome_mes = f'Mes_{mes:02d}'  # Gera Mes_01, Mes_02, ..., Mes_12
        caminho_completo = os.path.join(base_path, tipo, nome_mes)
        os.makedirs(caminho_completo, exist_ok=True)
        
print("Estrutura de pastas garantida.")

# copiar um arquivo para 'Mes_01' da NF-e
origem = r'C:\Sefaz_RPA\img'
destino = os.path.join(base_path, r'Consulta de NF-e Emitida\Recebida\Mes_01\Consulta.csv')

if os.path.isfile(origem):
    shutil.copy(origem, destino)
    print("Arquivo copiado com sucesso.")
else:
    print("Arquivo de origem não encontrado.")
