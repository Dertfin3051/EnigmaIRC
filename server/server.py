from flask import Flask, request
import json
import logging

with open("config.json", "r", encoding = 'utf-8') as config_file:  # Открываем файл конфига
    config = json.loads(config_file.read())  # Читаем и парсим конфиг

app = Flask("EnigmaIRC Server")  # Создаём приложение
debug = False


def checkNotNull(*args):    # Проверка любого кол-ва переменных на существование (aka NotNull)
    for var in args:    # Перебор аргументов
        if var is None:    # Если аргумент пустой - вернуть False
            return False
    return True    # Если все итерации прошли успешно, None(null) значений не было. Вернуть True

# Отключение авто-логов
app.logger.disabled = config["disable_request_logs"]
log = logging.getLogger("werkzeug")
log.disabled = config["disable_request_logs"]

session_status = []    # Важная переменная. Хранит актуальное кол-во отправленных сообщений. Если у клиента сообщений меньше, чем на сервере, то срабатывает триггер на получение нового сообщения
for i in range(config["session_count"]):
    session_status.append(0)    # Заполнение нулями


@app.route("/")  # Переход на основную страницу возвращает конфиг
def main():
    return config


"""
Структура отправки сообщения:
session = номер сессии
user = отображаемое имя пользователя
msg = зашифрованное содержимое сообщения

Пример : http://127.0.0.1/message/new?session=0&user=Name&msg=Message
"""


@app.route("/message/new")  # Отправка сообщения
def newMessage():
    # Получение аргументов из запроса
    session = request.args.get("session")
    user = request.args.get("user")
    msg = request.args.get("msg")

    if not checkNotNull(session, user, msg):    # Если хотябы один элемент не указан, отмена сообщения
        return "Ошибка: параметры сообщения не указаны"

    session_status[int(session)] += 1    # Обновление сессии

    filename = f"sessions/{str(session)}.json"  # Получаем путь к файлу по номеру сессии
    writeMessage(filename, user, msg)  # Сохраняем сообщение
    print(f"{user} отправил сообщение, как пользователь {session}.")  # Лог
    return "Сообщение отправлено"


"""
Структура получения сообщения:
session = номер сессии

Пример : http://127.0.0.1/message/get?session=0
"""


@app.route("/message/get")  # Получение сообщения по номеру сессии
def getMessage():
    session = request.args.get("session")
    if not checkNotNull(session):
        return "Ошибка: не указан номер сессии"
    filename = f"sessions/{str(session)}.json"
    return readMessage(filename)


@app.route("/sessions")    # Получение всех сессий
def getSessions():
    return session_status


async def writeMessage(file, user, msg):  # Сохранение сообщения
    message_data = {
        "user": user,
        "msg": msg
    }  # Формирование класса
    with open(file, "w", encoding = "utf-8") as msg_file:
        await msg_file.write(json.dumps(message_data))  # Запись файла с конвертацией в JSON


async def readMessage(file):
    with open(file, "r", encoding = "utf-8") as msg_file:
        message = await json.loads(msg_file.read())
    return message

print("Сервер запущен с {}:{}".format(config["server_public_ip"], config["port"]))
app.run(debug = debug, host = config["server_public_ip"],port = config["port"])

