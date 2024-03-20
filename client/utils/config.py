import json

def getConfig(path="config.json"):
    """
    Получение конфига.
    """
    with open("config.json", "r", encoding = "utf-8") as config_file:
        config = json.loads(config_file.read())
    return config


def saveConfig(data, path="config.json"):
    """
        Сохранение конфига.
    """
    with open("config.json", "w", encoding = "utf-8") as config_file:
        config_file.write(json.dumps(data, indent = 4))

def getServerConfig():
    """
    Получает конфигурацию сервера
    """
    local_config = getConfig()    # Получение локального конфига
    server_url = "http://" + local_config["server_ip"] + "/"
    import requests
    r = requests.get(server_url)    # Обращение к серверу
    return json.loads(r.text)    # Возвращаем конфиг

def getEncryption():
    """
    Получает ключ шифрования из конфига и создаёт класс шифрования с учётом возможных ошибок
    """
    from cryptography.fernet import Fernet
    from colorama import Fore
    config = getConfig()
    try:
        crypt = Fernet(bytes(config["MESSAGE_ENCRYPTION_KEY"], "utf-8"))  # Инициализация класса шифрования
    except ValueError:
        print(Fore.RED + "Некорректный ключ шифрования! " + Fore.RESET)
        print(f"{Fore.RED}Используйте {Fore.YELLOW}keygen {Fore.RED}для генерации ключа и добавьте его в конфиг")
        input()
        exit(0)
    return crypt