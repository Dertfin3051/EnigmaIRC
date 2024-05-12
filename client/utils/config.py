import json

import cryptography.fernet


def get_config(path="config.json") -> dict:
    """
    Получение конфига.
    """
    with open("config.json", "r", encoding = "utf-8") as config_file:
        config = json.loads(config_file.read())
    return config


def save_config(data, path="config.json") -> None:
    """
        Сохранение конфига.
    """
    with open("config.json", "w", encoding = "utf-8") as config_file:
        config_file.write(json.dumps(data, indent = 4))

def get_server_config():
    """
    Получает конфигурацию сервера
    """
    server_url = get_server_url()
    import requests
    r = requests.get(server_url)    # Обращение к серверу
    return json.loads(r.text)    # Возвращаем конфиг

def get_encryption() -> cryptography.fernet.Fernet:
    """
    Получает ключ шифрования из конфига и создаёт класс шифрования с учётом возможных ошибок
    """
    from cryptography.fernet import Fernet
    from colorama import Fore
    config = get_config()
    try:
        crypt = Fernet(bytes(config["MESSAGE_ENCRYPTION_KEY"], "utf-8"))  # Инициализация класса шифрования
    except ValueError:
        print(Fore.RED + "Некорректный ключ шифрования! " + Fore.RESET)
        print(f"{Fore.RED}Используйте {Fore.YELLOW}keygen {Fore.RED}для генерации ключа и добавьте его в конфиг")
        input()
        exit(0)
    return crypt

def check_for_version():
    from colorama import Fore
    local_config = get_config()
    server_config = get_server_config()
    if not (local_config["app_version"] == server_config["app_version"]):
        print(f"{Fore.YELLOW}Версия клиента {Fore.RED}({local_config['app_version']}){Fore.YELLOW} не совпадает с версией сервера {Fore.GREEN}({server_config['app_version']})")
        print(f"{Fore.YELLOW}Это может привести к ошибкам.\n" + Fore.RESET)

def get_server_url() -> str:
    config = get_config()
    server_url = "http://" + config["server_ip"] + "/"
    return server_url
