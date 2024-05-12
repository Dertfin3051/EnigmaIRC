from utils.config import *
from utils import connection
import utils.setup as setup
from utils.server_user_data_sync import *
from utils.handlers import *

debug = False

set_windows_console_title("Sender - EnigmaIRC")    # Установка заголовка окна (только для Windows)

config = get_config()
server_url = get_server_url()

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
except:
    pass
from cryptography.fernet import Fernet

crypt = get_encryption()    # Получение класса шифрования


# Получение кол-ва сессий
server_config = get_server_config()

check_for_version()    # Проверка на актуальность версии

# Получение данных
name = input("Имя пользователя: ")    # Имя пользователя
session = get_session(server_config)    # Номер сессии

# Ход работы
print("Авторизация...")
send_message("Авторизовался", session, name, debug=debug)
while True:
    msg = input(">>> ")
    send_message(msg, session, name, debug=debug)
