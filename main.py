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
from src.metrica import Metrica
import websocket
import ssl
import json




delay = 100

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
    try:
        botID = os.environ['telegram_botid']
        token = os.environ['telegram_token']
        url = f'https://api.telegram.org/{botID}:{token}/sendMessage'
        chat_id = -1001610705904
        topico = 768150
        msg = TelegramMsg(chat_id,topico,mensagem,"html")
        headers = {'Content-type': 'application/json'}
        print(msg.toJSON())
        requests.post(url, data=msg.toJSON(),headers=headers)
    except:
        print("Erro ao enviar mensagem no telegram")

def googleApiChat(mensagem):
    try:
        url = os.environ['google_webhook']
        app_message = {"text": mensagem}
        headers = {'Content-type': 'application/json'}
        return requests.post(url, data=dumps(app_message),headers=headers)
    except:
        print("Erro ao enviar mensagem ao google")


def tentar_executar(funcao, max_tentativas=3):
    tentativas = 0
    ultima_excecao = None
    while tentativas < max_tentativas:
        try:
            resultado = funcao()
            return resultado
        except Exception as e:
            tentativas += 1
            ultima_excecao = e
            print(f"Tentativa {tentativas} falhou: {e}")
            if tentativas < max_tentativas:
                print("Tentando novamente...")
                time.sleep(5)
    raise Exception("Número máximo de tentativas alcançado. A função falhou todas as vezes.") from ultima_excecao

try:
    print("Iniciando consulta do portal do CNJ")
    metrica = tentar_executar(lambda : Metrica())
    sevenMinutes = datetime.strptime('00:07:00.00', '%H:%M:%S.%f')
    latencia = datetime.strptime(metrica.latenciaExtrator, '%H:%M:%S.%f')
    if(latencia > sevenMinutes):
        print(f"O extrator esta com lag! tempo registrado no CNJ {latencia.strftime('%H:%M:%S.%f')}")
        googleApiChat(f"O extrator esta com lag! tempo registrado no CNJ {latencia.strftime('%H:%M:%S.%f')}")
        telegramMsg(f"O extrator esta com lag! tempo registrado no CNJ {latencia.strftime('%H:%M:%S.%f')}")
    else:
        print("Data Menor que 7 minutos")
except Exception:
    print("--- Erro detectado ---")
    traceback.print_exception()
    telegramMsg("Erro ao obter metricas no CNJ")
    googleApiChat("Erro ao obter metricas no CNJ")
