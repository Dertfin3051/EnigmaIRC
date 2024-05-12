import json

def check_not_null(*args):  # Проверка любого кол-ва переменных на существование (aka NotNull)
    for var in args:  # Перебор аргументов
        if var is None:  # Если аргумент пустой - вернуть False
            return False
    return True  # Если все итерации прошли успешно, None(null) значений не было. Вернуть True


async def write_message(file, username, message):  # Сохранение сообщения
    message_data = {
        "user": username,
        "msg": message
    }  # Формирование класса
    with open(file, "w", encoding="utf-8") as msg_file:
        await msg_file.write(json.dumps(message_data))  # Запись файла с конвертацией в JSON

def get_config():
    with open("config.json", "r", encoding='utf-8') as config_file:  # Открываем файл конфига
        config = json.loads(config_file.read())  # Читаем и парсим конфиг
    return config

def generate_empty_sessions():
    config = get_config()
    session_status = []
    for i in range(config["session_count"]):
        session_status.append(0)  # Заполнение нулями
    return session_status


async def read_message(file):
    with open(file, "r", encoding="utf-8") as msg_file:
        message = await json.loads(msg_file.read())
    return message