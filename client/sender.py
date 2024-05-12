from utils.config import *
from utils import connection
import utils.setup as setup
from utils.server_user_data_sync import *

try:

    import win32api

    import platform
    if platform.system() == "Windows":
        win32api.SetConsoleTitle("Sender - EnigmaIRC")
except:
    pass

debug = False

config = get_config()
server_url = "http://" + config["server_ip"] + "/"

connection.connect()    # Программа не запустится до подключения к сети
connection.try_server_connection(server_url)    # Программа не запустится, если сервер недоступен

if config["isFirstLaunch"]:    # Установка библиотек при первом запуске
    setup.setup()

# Импорты
import requests
import colorama
colorama.init()
try:
    colorama.just_fix_windows_console()
except Exception:
    pass
from cryptography.fernet import Fernet

crypt = get_encryption()    # Получение класса шифрования


def send(msg: str, session, name):    # Функция отправки сообщения
    if msg == "":
        print("Вы не можете отправлять пустые сообщения!")
        return
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
server_config = get_server_config()

check_for_version()    # Проверка на актуальность версии

# Получение данных
name = input("Имя пользователя: ")    # Имя пользователя
session = get_session(server_config)    # Номер сессии

# Ход работы
print("Авторизация...")
send("Авторизовался", session, name)
while True:
    msg = input(">>> ")
    send(msg, session, name)
