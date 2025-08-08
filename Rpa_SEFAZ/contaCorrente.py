from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import anticaptcha
import resolvebase64
import json
import database
import DatasMes
import modificaCsv
import base64
import os
import shutil
from datetime import datetime

hoje = datetime.now()
mesAtual = hoje.month
if mesAtual < 10:
    mesAtual = f'0{mesAtual}'
anoAtual = hoje.year

#pega as informacoes que estao no json
#--------------json----------------
with open('json\contabilista.json', 'r') as file:
    dados = json.load(file)
userContabilista = dados["Contabilista"]
senhaContabilista = dados["SenhaContabilista"]

#setando datas de consulta
#---------------data-------------------
mesPassado, anoPassado = DatasMes.dataContaCorrente()

#---------------------------------------
#pegando uma lista com o grupo, filliais e cnpj do banco de dados
lista_InscEstd = database.retornoInscEstd()

#-----------caminho download-------------------
caminho = fr'C:\RPA_NFE_CTE\Sefaz_RPA\downloads\png'

def mainNfe():
    #setando opçoes no chromedriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
    "download.default_directory": caminho,
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
    LoginEcaptcha(driver)
    loopNfe(driver,lista_InscEstd)

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
                #print(src)
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

def loopNfe(driver,lista_InscEstd):
    try:
        for InscEstd in lista_InscEstd:

            while True:
            
                '''if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[0])
                    driver.close()'''
                #abre uma nova aba com o link da consulta de nfe
                driver.execute_script("window.open('');")
                sleep(1)

                WebDriverWait(driver, 10).until(lambda driver: len(driver.window_handles) > 1)
                driver.switch_to.window(driver.window_handles[1])
                driver.get('https://www.sefaz.mt.gov.br/ccfiscal/lancamento/consulta')
                sleep(1)
                dadosInscEstd(driver,InscEstd)
                sleep(1)
                break
    except Exception as e:
        pass

def dadosInscEstd(driver,InscEstd):
    inscricaoEstadual = InscEstd[0].strip()
    filial = InscEstd[1].strip()
    
    NumDoc = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.NAME, "numeroPessoaContribuinte")))
    NumDoc.send_keys(inscricaoEstadual)

    select_mes = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "mesInicio")))
    selectMes = Select(select_mes)
    selectMes.select_by_value(str(mesPassado))

    select_ano = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "anoInicio")))
    selectAno = Select(select_ano)
    selectAno.select_by_value(str(anoPassado))

    pesquisarNumDoc = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "bttnPesquisar")))
    pesquisarNumDoc.click()

    sleep(5)

    try:
        elemento = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Erro inesperado')]")))
        
        print("Elemento encontrado:", elemento.text)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print('aba fechada')
    except:

        pesquisar = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "botaoConfirmar")))
        pesquisar.click()
        sleep(5)
    
        pdf = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True
        })
        #------------------------------------
        # salvando pagina para pdf
        #------------------------------------
        caminhoInsc = fr"downloads\png\mes_{mesAtual}\Conta_Corrente_{mesAtual}.{anoAtual}_{filial}.pdf"

        with open(caminhoInsc, "wb") as f:
            f.write(base64.b64decode(pdf['data']))

        if os.path.exists(caminhoInsc):    
            print(f'Conta Corrente {inscricaoEstadual} salva com sucesso!')
            caminhoPadrao = fr'C:\SPED_fiscal\Conta Corrente\mes_{mesAtual}'

            shutil.copy(caminhoInsc, fr'{caminhoPadrao}\Conta_Corrente_{mesAtual}.{anoAtual}_{filial}.pdf')

            print(fr"Arquivo foi copiado para a pasta: {caminhoPadrao}\Conta_Corrente_{mesAtual}.{anoAtual}_{filial}.pdf")                          
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print('aba fechada')

    return

if __name__ == "__main__":
    mainNfe()