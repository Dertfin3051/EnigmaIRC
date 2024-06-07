import time

import cryptography.fernet

from utils.config import *
from utils import connection
import utils.setup as setup
from utils.server_user_data_sync import *
from utils.handlers import *

set_windows_console_title("Listener - EnigmaIRC")    # Установка заголовка окна (только для Windows)

config = get_config()
server_url = get_server_url()

connection.connect()    # Программа не запустится до подключения к сети
connection.try_server_connection(server_url)    # Программа не запустится, если сервер недоступен

if config["isFirstLaunch"]:    # Установка библиотек при первом запуске
    setup.setup()

# Импорты
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import colorama

colorama.init()
try:
    colorama.just_fix_windows_console()
except:
    pass

from cryptography.fernet import Fernet
crypt = get_encryption()    # Получение класса шифрования

local_sessions = requests.get(f"{server_url}sessions").json()    # Получаем информацию о всех сессиях
# Получение кол-ва сессий
server_config = get_server_config()

check_for_version()    # Проверка на актуальность версии

username = get_username()    # Имя пользователя
session = get_session(server_config)    # Номер сессии

actual_sessions_client = requests.Session()
# Избежание ошибки о максимальном кол-ве попытокS
retry = Retry(connect=999999999999, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
actual_sessions_client.mount('http://', adapter)
actual_sessions_client.mount('https://', adapter)
while True:
    # Получаем информацию об актуальных сессиях
    actual_sessions = actual_sessions_client.get(f"{server_url}sessions").json()
    i = 0
    for i in range(len(actual_sessions)):    # Пробегаем по актуальным сессиям
        if actual_sessions[i] != local_sessions[i]:  # Несостыковка сессий = отправлено новое сообщение
            handle_new_message(crypt, session, i, username)
            # Обновляем локальные сессии
            local_sessions[i] += 1
            time.sleep(1)  # Задержка
