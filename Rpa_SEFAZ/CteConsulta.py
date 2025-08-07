from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import anticaptcha
import resolvebase64
import json
import database


#pega as informacoes que estao no json
#--------------json----------------
with open('json\contabilista.json', 'r') as file:
    dados = json.load(file)

userContabilista = dados["Contabilista"]
senhaContabilista = dados["SenhaContabilista"]

#setando opçoes no chromedriver
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

#----------Comecando login----------------
def LoginEcaptcha(driver):
    try:
        tipoUsuario = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'formLogin:selectTipoUsuario_label')))
        tipoUsuario.click()

        # Depois espera o item 'Contabilista' ficar visível e clica
        contabilista = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'formLogin:selectTipoUsuario_1')))

        contabilista.click() 
        sleep(2)
        #tenta resolver o captcha 5x, caso nao consiga, ele fecha o programa
        cnpjs = database.retornoCnpj()
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
                senha.clear()
                senha.send_keys(senhaContabilista)
                sleep(2)

#------------------------------------------------------
                #resolvendo o captcha na sefaz
                captcha_element = driver.find_element(By.XPATH, '//img[contains(@src, "data:image/png;base64")]')
                # Pegando o atributo src
                src = captcha_element.get_attribute('src')
                print(src)
                #o decode64 pega a imagem que vem em base 64 e converte em jpg
                resolvebase64.decode64(src)
                sleep(1)
                #anticaptcha resolve o captch
                captcha = anticaptcha.anticaptcha()

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
                #Verifica se ocorreu algum erro
                #se eocorreu tenta novamente
                try:
                    erro = None
                    erro = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'ui-messages-error')))
                except:
                    pass
                if erro:
                    continue

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
