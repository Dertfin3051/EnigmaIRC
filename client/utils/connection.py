import time

import requests

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