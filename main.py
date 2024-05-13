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






def getMetricas() :
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("window-size=1400,2100") 
    chrome_options.add_argument('--disable-gpu')

    driver=webdriver.Chrome(options=chrome_options)
    driver.get("https://paineisanalytics.cnj.jus.br/single/?appid=4a2b72d3-1b68-4c5e-b6fc-5b92f28dc45c&sheet=d2c4c0b8-6f24-47d3-b464-2079ce604f2c&theme=horizon&lang=pt-BR&opt=ctxmenu,currsel")
    delay = 100

    xpath = "/html/body/div[4]/div/div[2]/div/article/div/div[8]/div/article/div[1]/div/div/qv-filterpane/div/div/div/div[2]/span"

    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        print("done")
    except TimeoutException:
        print("Loading took too much time!")


    try: 
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(3)
        focused_elem = driver.switch_to.active_element.send_keys("TJRO")
        time.sleep(2)
        tjroFilter = "/html/body/div[7]/div/div/div/ng-transclude/div/div[3]/div/article/div[1]/div/div/div/div[2]/div[1]/div/ul/li[1]"
        driver.find_element(By.XPATH, tjroFilter).click()
        time.sleep(2)
        atualizadoEmPath = "/html/body/div[4]/div/div[2]/div/article/div/div[3]/div/article/div[1]/div/div/div/button/text/span"
        latenciaTjRoPath = "/html/body/div[4]/div/div[2]/div/article/div/div[10]/div/article/div[1]/div/div/div/div/div/div[2]/div/div/div[1]/div/span"
        latenciaExtratorPath = "/html/body/div[4]/div/div[2]/div/article/div/div[11]/div/article/div[1]/div/div/div/div/div/div[2]/div/div/div[1]/div/span"
        latenciaConversorPath = "/html/body/div[4]/div/div[2]/div/article/div/div[12]/div/article/div[1]/div/div/div/div/div/div[2]/div/div/div[1]/div/span"
        

        latenciaExtrator = driver.find_element(By.XPATH, latenciaExtratorPath).text
        print("--- Relatorio ---")
        print(driver.find_element(By.XPATH, atualizadoEmPath).text)
        print("Latencia TJRO: " + driver.find_element(By.XPATH, latenciaTjRoPath).text)
        print("Latencia Extrator: " + latenciaExtrator)
        print("Latencia Conversor: " + driver.find_element(By.XPATH, latenciaConversorPath).text)
    except Exception:
        print(traceback.format_exc())
        print("Erro")

    driver.close()
    return datetime.strptime(latenciaExtrator, '%H:%M:%S.%f')

class TelegramMsg:
    def __init__(self,chatId,messageThreadId,text,parseMode):
        self.chat_id = chatId
        self.message_thread_id = messageThreadId
        self.text = text
        self.parse_mode = parseMode
    
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)

def telegramMsg(mensagem):
    botID = os.environ['telegram_botid']
    token = os.environ['telegram_token']
    url = f'https://api.telegram.org/{botID}:{token}/sendMessage'
    chat_id = -1001610705904
    topico = 768150
    msg = TelegramMsg(chat_id,topico,mensagem,"html")
    headers = {'Content-type': 'application/json'}
    print(msg.toJSON())
    return requests.post(url, data=msg.toJSON(),headers=headers)

def googleApiChat(mensagem):
    url = os.environ['google_webhook']
    app_message = {"text": mensagem}
    headers = {'Content-type': 'application/json'}
    return requests.post(url, data=dumps(app_message),headers=headers)

try:
    sevenMinutes = datetime.strptime('00:07:00.00', '%H:%M:%S.%f')
    latencia = getMetricas()
    if(latencia > sevenMinutes):
        googleApiChat(f"O extrator esta com lag! tempo registrado no CNJ {latencia.strftime('%H:%M:%S.%f')}")
        telegramMsg(f"O extrator esta com lag! tempo registrado no CNJ {latencia.strftime('%H:%M:%S.%f')}")
    else:
        print("Data Menor que 7 minutos")
except Exception:
    print(traceback.format_exc())
    telegramMsg("Erro ao obter metricas no CNJ")
    googleApiChat("Erro ao obter metricas no CNJ")
