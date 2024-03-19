import json

def getConfig(path="config.json"):
    """
    Получение конфига.
    """
    with open("config.json", "r", encoding = "utf-8") as config_file:
        config = json.loads(config_file.read())
    return config


def saveConfig(data, path="config.json"):
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