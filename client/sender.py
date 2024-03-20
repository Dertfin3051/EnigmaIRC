import os

from utils.config import *
from utils import connection
import utils.setup as setup
from utils.serverUserDataSync import *

debug = False

config = getConfig()
server_url = "http://" + config["server_ip"] + "/"

connection.connect()    # Программа не запустится до подключения к сети

if config["isFirstLaunch"]:    # Установка библиотек при первом запуске
    setup.setup()

# Импорты
import requests
import colorama
colorama.init()
colorama.just_fix_windows_console()
from cryptography.fernet import Fernet

crypt = getEncryption()    # Получение класса шифрования

def send(msg: str, session, name):    # Функция отправки сообщения
    msg = crypt.encrypt(bytes(msg, "utf-8"))    # Шифруем сообщение
    params = {
        "session": session,
        "user": name,
        "msg": msg
    }    # Записываем параетры
    req = requests.get(f"{server_url}message/new", params = params)    # Посылаем запрос

    if debug: print(f"Отправлено\nЗашафрованное сообщение: {msg}\n")    # Отправка зашифрованного сообщения отправителю
    return req    # И на всякий статус. Хз зачем, пусть будет, так типо правильно

# Получение кол-ва сессий
server_config = getServerConfig()

checkForVersion()    # Проверка на актуальность версии

# Получение данных
name = input("Имя пользователя: ")    # Имя пользователя
session = getSession(server_config)    # Номер сессии

# Ход работы
print("Авторизация...")
send("Авторизовался", session, name)
while True:
    msg = input(">>> ")
    send(msg, session, name)
