import cryptography.fernet
import requests
from config import *
import colorama

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
    elif message == "Авторизовался":
        message = "Авторизовался "    # Защита от поддельных сообщений об авторизации
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


def print_encrypted_message(user_session: int, sender_session: int, user_name: str, sender_name: str, message_context: str) -> None:
    """
    :param user_session: Сессия пользователя, у которого запущен listener
    :param sender_session: Сессия пользователя, который отправил сообщение
    :return: None
    """
    msg_color = colorama.Fore.LIGHTBLUE_EX

    if f"@{user_name}" in message_context:
        msg_color = colorama.Fore.LIGHTYELLOW_EX

    if sender_session != user_session:  # Сообщение отправил другой пользователь
        print(colorama.Fore.LIGHTBLUE_EX + f"{sender_name} => {message_context}" + colorama.Fore.RESET)
    else:  # Сообщение отправил этот пользователь
        print(colorama.Fore.WHITE + f"Вы => {message_context}" + colorama.Fore.RESET)
    # TODO: Добавить @ping пользователя


def handle_new_message(crypt: cryptography.fernet.Fernet, user_session: int, sender_session: int, username_runned_by: str):
    msg_data = requests.get(f"{get_server_url()}message/get", params={"session": sender_session}).json()
    msg = msg_data["msg"]
    try:
        msg = bytes.decode(crypt.decrypt(bytes(msg, 'utf-8')))  # Расшифровываем
        print_encrypted_message(user_session, sender_session, username_runned_by,msg_data['user'], msg)
    except cryptography.fernet.InvalidToken:
        print(colorama.Fore.RED + "Не удалось расшифровать входящее сообщение. Возможно доступ к чату получен извне! ")