from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import anticaptcha
import resolvebase64
import json
import pandas as pd
from datetime import datetime
import os
import glob


#pega as informacoes que estao na 
#--------------json----------------
with open('json\contabilista.json', 'r') as file:
    dados = json.load(file)

userContabilista = dados["contabilista"]
senhaContabilista = dados["senha_contabilista"]





options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
"download.default_directory": "document/xls/",
#
"download.prompt_for_download": False,
"download.directory_upgrade": True,
"safebrowsing.enabled": True
})
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--mute-audio')
driver = webdriver.Chrome(options=options)
url = "https://www.sefaz.mt.gov.br/acesso/pages/login/login.xhtml"
driver.implicitly_wait(2)
driver.get(url)

try:
    tipoUsuario = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'formLogin:selectTipoUsuario_label')))
    tipoUsuario.click()

    # Depois espera o item 'Contabilista' ficar visível e clica
    contabilista = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'formLogin:selectTipoUsuario_1')))

    contabilista.click() 
    sleep(2)
    for x in range(5):
        try:
            crc = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'formLogin:inputLogin'))
            )
            crc.clear()
            sleep(1)
            crc.send_keys(userContabilista)

            senha = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'formLogin:inputSenha'))
            )
            senha.send_keys(senhaContabilista)
            sleep(2)

            #----------------------------
            #resolvendo o captcha na sefaz
            captcha_element = driver.find_element(By.XPATH, '//img[contains(@src, "data:image/png;base64")]')
            # Pegando o atributo src
            src = captcha_element.get_attribute('src')
            #o decode64 pega a imagem que vem em base 64 e converte em jpg
            resolvebase64.decode64(src)
            sleep(1)
            #anticaptcha resolve o captch
            captcha = anticaptcha()
            print(captcha)

            #a enviar captcha resolvido
            captchaResolvido = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'formLogin:inputCaptcha'))
            )
            captchaResolvido.clear()
            captchaResolvido.send_keys(captcha)
            sleep(2)
            

            efetuarLogin = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Efetuar Login')]"))
            )
            efetuarLogin.click() 

            #-----------------------------------
            #tenta ver se ocorreu algum erro
            #se eocorreu tenta novamente
            try:
                erro = None
                #erro = driver.find_element(By.CLASS_NAME, 'ui-messages-error')
                erro = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'ui-messages-error')))
            except:
                pass
            if erro:
                continue
            #---------------------------

            #-----------------------------------
            #tenta ver se existe a tela de sessao duplicada
            #se a sessao esta duplicada, substitue e acessa            
            try:
                outraSessaoAberta = None
                outraSessaoAberta = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[contains(@id, 'superPanelMensagem')]"))
                )
            except:
                pass
            if outraSessaoAberta:
                senhaSessao = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password'].ui-password"))
                )
                senhaSessao.send_keys(senhaContabilista)

                substituir  = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input.btnPadrao[value='Substituir']"))
                )
                substituir.click()
                break
            #---------------------------

            try:
                telaInicial = None 
                telaInicial = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "tst"))
                )
            except:
                pass
            
            if telaInicial:
                break
            else:
                pass
    
        except:
            pass
    print('Pasou do login com exito!')
    #print(cnpjs)
except Exception as e:
    print('Erro ao tentar logar')
    print(e)

#
#ACESSANDO A CONSULTA DE NFE
#

try:
       
        for cnpj in cnpjs:
            while True:
                print(cnpj[0])
                
                '''if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[0])
                    driver.close()'''
                #abre uma nova aba com o link da consulta de nfe
                driver.execute_script("window.open('');")
                sleep(1)

                WebDriverWait(driver, 10).until(lambda driver: len(driver.window_handles) > 1)
                driver.switch_to.window(driver.window_handles[1])
                driver.get('https://www.sefaz.mt.gov.br/nfe/pages/consultaemitidasrecebidas/consultaemitidasrecebidas.xhtml')
                sleep(1)


except Exception as e:
    print('Erro ao tentar acessar a consulta de NFe')
    print(e)

    # conversor de XLS para CVS


agora = datetime.now()
mes = agora.month
ano = agora.year

grupo = 16
filial = 1008053

# Caminho da sua pasta
pasta_xls = r"C:\Users\rafael.r.santos\Desktop\teste_XLS\XLS"
pasta_csv = (r'C:\Users\rafael.r.santos\Desktop\teste_XLS\CSV')

# Busca todos os arquivos .XLS na pasta
arquivos_xls = glob.glob(os.path.join(pasta_xls, '*.xls'))

for arquivo_xls in arquivos_xls:
    nome_arquivo = os.path.basename(arquivo_xls)
    
    # Ler o arquivo .xls usando o caminho completo
    df = pd.read_excel(arquivo_xls)
    
    # Criar nome para o CSV com dados da variável e nome do arquivo original (opcional)
    arquivo_csv = (f"NFe{grupo}_{filial}_{mes}{ano}.csv")
    

    caminho_csv = os.path.join(pasta_csv, arquivo_csv)
    
    # Salvar como .csv
    df.to_csv(caminho_csv, index=False)
    
    print(f"Arquivo convertido e salvo como {arquivo_csv}")
