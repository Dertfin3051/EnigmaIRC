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
except AttributeError:
    pass

from cryptography.fernet import Fernet
crypt = get_encryption()    # Получение класса шифрования

local_sessions = requests.get(f"{server_url}sessions").json()    # Получаем информацию о всех сессиях
# Получение кол-ва сессий
server_config = get_server_config()

check_for_version()    # Проверка на актуальность версии

session = get_session(server_config)    # Номер сессии

actual_sessions_client = requests.Session()
# Избежание ошибки о максимальном кол-ве попыток
retry = Retry(connect=999999999999, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
actual_sessions_client.mount('http://', adapter)
actual_sessions_client.mount('https://', adapter)
while True:
    actual_sessions = actual_sessions_client.get(f"{server_url}sessions").json()    # Получаем информацию об актуальных сессиях
    i = 0
    for i in range(len(actual_sessions)):    # Пробегаем по актуальным сессиям
        if actual_sessions[i] != local_sessions[i]:  # Несостыковка сессий = отправлено новое сообщение
            # Получаем и выводим новое сообщение
            msg_data = requests.get(f"{server_url}message/get", params = {"session": i}).json()
            msg = msg_data["msg"]
            try:
                msg = bytes.decode(crypt.decrypt(bytes(msg, 'utf-8')))    # Расшифровываем
                if i != session:    # Сообщение отправил другой пользователь
                    print(colorama.Fore.LIGHTBLUE_EX + f"{msg_data['user']} => {msg}" + colorama.Fore.RESET)
                else:    # Сообщение отправил этот пользователь
                    print(colorama.Fore.WHITE + f"Вы => {msg}" + colorama.Fore.RESET)
            except cryptography.fernet.InvalidToken:
                print(colorama.Fore.RED + "Не удалось расшифровать входящее сообщение. Возможно доступ к чату получен извне! ")


            # Обновляем локальные сессии
            local_sessions[i] += 1
            time.sleep(1)  # Задержка