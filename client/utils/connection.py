import time

import requests
from colorama import Fore

CONNECTION_TRYING_DELAY = 2

# Проверка подключения к сети
def connect():
    while True:
        try:
            r = requests.get("http://google.com")
            break
        except requests.exceptions.ConnectionError:
            print("Не удаётся подключиться к сети...")
            time.sleep(CONNECTION_TRYING_DELAY)
            print("Переподключение...", end = "\n\n")

def try_server_connection(server_url: str):
    import requests
    try:
        requests.get(server_url)
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "Не удаётся подключиться к серверу. Возможно, вы забыли указать данный параметр!")
        input()
        exit(0)