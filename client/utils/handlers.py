import requests
from config import *

def set_windows_console_title(title: str):
    try:

        import win32api

        import platform
        if platform.system() == "Windows":
            win32api.SetConsoleTitle(title)
    except:
        pass

def send_message(message: str, session, name, **kwargs):    # Функция отправки сообщения
    server_url = get_server_url()
    crypt = get_encryption()
    if message == "":
        print("Вы не можете отправлять пустые сообщения!")
        return
    encrypted_message = crypt.encrypt(bytes(message, "utf-8"))    # Шифруем сообщение
    params = {
        "session": session,
        "user": name,
        "msg": encrypted_message
    }    # Записываем параетры
    req = requests.get(f"{server_url}message/new", params = params)    # Посылаем запрос

    for debug in kwargs.items():
        debug = kwargs["debug"]
        if debug: print(f"Отправлено\nЗашафрованное сообщение: {encrypted_message}\n")    # Отправка зашифрованного сообщения отправителю
    return req    # И на всякий статус. Хз зачем, пусть будет, так типо правильно