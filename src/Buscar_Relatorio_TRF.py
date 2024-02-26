from tkinter import filedialog
import pandas as pd
from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from abc import ABC
import time
import os
import json
import tkinter
import menssage.Pidgin as Pidgin

class PageElement(ABC):
    def __init__(self, driver, url='') -> None:
        self.driver = driver
        self.url = url

    def open(self):
        self.driver.get(self.url)


class Login(PageElement):
    prestador = (By.XPATH, '//*[@id="conteudo"]/ul/li[2]/a')
    usuario = (By.XPATH, '//*[@id="txbUsuario"]')
    senha = (By.XPATH, '//*[@id="txbSenha"]')
    entrar = (By.XPATH, '//*[@id="btnAcessar"]')

    def exe_login(self, usuario, senha):
        self.driver.find_element(*self.prestador).click()
        time.sleep(1)
        self.driver.find_element(*self.usuario).send_keys(usuario)
        self.driver.find_element(*self.senha).send_keys(senha)
        time.sleep(1)
        self.driver.find_element(*self.entrar).click()

class Caminho(PageElement):
    relatorio = (By.XPATH, '//*[@id="menutopo"]/ul/li[2]/a')
    listagem = (By.XPATH, '//*[@id="ctl00_conteudo_lblTitulo2"]')
    pesquisar = (By.XPATH, '//*[@id="ctl00_conteudo_btnPesquisar"]')

    def exe_caminho(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element(*self.relatorio).click()
        time.sleep(1)
        self.driver.find_element(*self.listagem).click()
        time.sleep(1)
        self.driver.find_element(*self.pesquisar).click()

    def apagarPDF_antigo(self):
        file_path = r"C:\PDF_TRF_SJ\reportdownload.pdf"

        if os.path.isfile(file_path):
            os.remove(file_path)
            print("PDF antigo Removido da pasta")
        else:
            print("Sem arquivo na pasta")

        

class Download(PageElement):
    relatorio = (By.XPATH, '//*[@id="menutopo"]/ul/li[2]/a')

    def exe_download(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(100)
        # Download(driver, url).detectar_download()

    # def detectar_download():
    #     lista_diretorio = os.listdir(r"\\10.0.0.239\automacao_faturamento\Faturamento_TRF")
    #     qtd_download = len(lista_diretorio)
    #     print(qtd_download)
    #     if(qtd_download == 0):
    #         time.sleep(200)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def Buscar_Carteirinha():
    global driver, url 
    try:
        url = 'https://prosocial.trf1.jus.br/e-prosocial/index.aspx'

        settings = {
            "recentDestinations": [{
                    "id": "Save as PDF",
                    "origin": "local",
                    "account": "",
                }],
                "selectedDestinationId": "Save as PDF",
                "version": 2
            }

        options = {
            'proxy' : {
                'http': 'http://lucas.timoteo:Caina8125@10.0.0.230:3128',
                'https': 'http://lucas.timoteo:Caina8125@10.0.0.230:3128'
            }
        }

        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
                "printing.print_to_pdf": True,
                "download.default_directory": r"C:\PDF_TRF_SJ",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False,
                "safebrowsing.disable_download_protection,": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "plugins.always_open_pdf_externally": True,
                "printing.print_preview_sticky_settings.appState": json.dumps(settings)
        })

        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--kiosk-printing')
        
        try:
            servico = Service(ChromeDriverManager().install())
            try:
                driver = webdriver.Chrome(service=servico, seleniumwire_options= options, options = chrome_options)
            except:
                driver = webdriver.Chrome(seleniumwire_options= options, options = chrome_options)
        except:
            driver = webdriver.Chrome(seleniumwire_options= options, options = chrome_options)

        usuario = "00735860000173"
        senha = "0073AMHPDFDF"

        login_page = Login(driver, url)
        login_page.open()
        login_page.exe_login(usuario, senha)
        time.sleep(1)
        Caminho(driver, url).exe_caminho()
        time.sleep(1)
        Caminho(driver, url).apagarPDF_antigo()
        time.sleep(1)
        Download(driver, url).exe_download()
        time.sleep(1)

    
    except Exception as err:
        tkinter.messagebox.showerror("Automação", f"Ocorreu uma exceção não tratada. \n {err.__class__.__name__} - {err}")

        Pidgin.TRF(f"Ocorreu uma exceção não tratada. \n {err.__class__.__name__} - {err}")

    driver.quit()