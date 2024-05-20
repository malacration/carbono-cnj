import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime
import time
from json import dumps
import traceback
import os


class Metrica:

    _searchInputPath = "//*[contains(text(), 'Clique para escolher o tribunal')]"
    _searchResultPath = "//*[contains(text(), 'TJRO')]//ancestor::li[1]"
    
    _latenciaOrigemPath = "//span[contains(text(), 'na origem')]//ancestor::div[contains(@class, 'sn-kpi ')]//div[contains(@class, 'sn-kpi-value')]//span[last()]"
    _latenciaExtratorPath = "//span[contains(text(), 'no extrator')]//ancestor::div[contains(@class, 'sn-kpi ')]//div[contains(@class, 'sn-kpi-value')]//span[last()]"
    _latenciaConversorPath = "//span[contains(text(), 'no conversor')]//ancestor::div[contains(@class, 'sn-kpi ')]//div[contains(@class, 'sn-kpi-value')]//span[last()]"
    
    latenciaOrigem : any
    latenciaExtrator : any
    latenciaConversor : any
    

    driver : webdriver
    delay = 100

    def __init__(self) -> None:
        self.driver = webdriver.Chrome(options=self._getChromeOptions())
        self.driver.get("https://paineisanalytics.cnj.jus.br/single/?appid=4a2b72d3-1b68-4c5e-b6fc-5b92f28dc45c&sheet=d2c4c0b8-6f24-47d3-b464-2079ce604f2c&theme=horizon&lang=pt-BR&opt=ctxmenu,currsel")
        self._waitingLoading()
        self._interagir()
        pass

    def _getChromeOptions(self):
        chrome_options=webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--disable-gpu')
        return chrome_options

    def _waitingLoading(self):
        self._uiAction(lambda : WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, self._searchInputPath))), "Esperando Pagina carregar")
        

    def _interagir(self):

        actionClick = lambda : self.driver.find_element(By.XPATH,self._searchInputPath).click()
        self._uiAction(actionClick,"Clicar no botao para inserir busca")

        actionSendKeys = lambda : self.driver.switch_to.active_element.send_keys("TJRO")
        self._uiAction(actionSendKeys,"Inserir termo de pesquisa")
        
        actionClickSearchResult = lambda : self.driver.find_element(By.XPATH, self._searchResultPath).click()
        self._uiAction(actionClickSearchResult,"Clica no resultado da Busca")
        self._uiAction(lambda : self._registraMetricas(),"Registra metricas")

        

    def _registraMetricas(self) : 
        self.latenciaExtrator = self.driver.find_element(By.XPATH, self._latenciaExtratorPath).text
        self.latenciaConversor = self.driver.find_element(By.XPATH, self._latenciaConversorPath).text
        self.latenciaOrigem = self.driver.find_element(By.XPATH, self._latenciaOrigemPath).text
        
    def _uiAction(self,action,actionMsg):
        try:
            print("Tentando: " + actionMsg)
            time.sleep(3)
            action()
            print("Finalizando: "+actionMsg)
        except Exception as e:
            raise Exception("Erro ao "+actionMsg) from e