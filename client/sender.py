from utils.config import *
from utils import connection
import utils.setup as setup
from utils.server_user_data_sync import *
from utils.handlers import *

debug = False
is_source_code = True    # False при билде приложения в бинарник

set_windows_console_title("Sender - EnigmaIRC")    # Установка заголовка окна (только для Windows)

config = get_config()
server_url = get_server_url()

connection.connect()    # Программа не запустится до подключения к сети
connection.try_server_connection(server_url)    # Программа не запустится, если сервер недоступен

if config["isFirstLaunch"] and is_source_code:    # Установка библиотек при первом запуске
    setup.setup()

# Импорты
import colorama
colorama.init()
try:
    colorama.just_fix_windows_console()
except:
    pass

crypt = get_encryption()    # Получение класса шифрования

server_config = get_server_config()    # Получение конфига сервера

check_for_version()    # Проверка на актуальность версии

# Получение данных
username = get_username()    # Имя пользователя
session = get_session(server_config)    # Номер сессии

# Ход работы
print("Авторизация...")
send_message("Авторизовался", session, username, debug=debug)
while True:
    msg = input(">>> ")
    send_message(msg, session, username, debug=debug)
