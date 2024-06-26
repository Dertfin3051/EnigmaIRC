import time

import cryptography.fernet

from utils.config import *
from utils import connection
import utils.setup as setup
from utils.serverUserDataSync import *
try:

    import win32api

    import platform
    if platform.system() == "Windows":
        win32api.SetConsoleTitle("Listener - EnigmaIRC")
except:
    pass

config = getConfig()
server_url = "http://" + config["server_ip"] + "/"

connection.connect()    # Программа не запустится до подключения к сети
tryServerConnection(server_url)    # Программа не запустится, если сервер недоступен

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
crypt = getEncryption()    # Получение класса шифрования

local_sessions = requests.get(f"{server_url}sessions").json()    # Получаем информацию о всех сессиях
# Получение кол-ва сессий
server_config = getServerConfig()

checkForVersion()    # Проверка на актуальность версии

session = getSession(server_config)    # Номер сессии

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