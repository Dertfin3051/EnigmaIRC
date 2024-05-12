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


async def read_message(file):
    with open(file, "r", encoding="utf-8") as msg_file:
        message = await json.loads(msg_file.read())
    return message