from flask import Flask, request
import json
import logging

app = Flask("EnigmaIRC Server")  # Создаём приложение
DEBUG = False

with open("config.json", "r", encoding='utf-8') as config_file:  # Открываем файл конфига
    config = json.loads(config_file.read())  # Читаем и парсим конфиг

# Отключение авто-логов
app.logger.disabled = config["disable_request_logs"]
log = logging.getLogger("werkzeug")
log.disabled = config["disable_request_logs"]

session_status = []  # Важная переменная. Хранит актуальное кол-во отправленных сообщений. Если у клиента сообщений меньше, чем на сервере, то срабатывает триггер на получение нового сообщения
for i in range(config["session_count"]):
    session_status.append(0)  # Заполнение нулями


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


@app.route("/")  # Переход на основную страницу возвращает конфиг
def config():
    return config


@app.route("/sessions")  # Получение всех сессий
def get_sessions():
    return session_status


"""
Структура получения сообщения:
session = номер сессии

Пример : http://127.0.0.1/message/get?session=0
"""
@app.route("/message/get")  # Получение сообщения по номеру сессии
def get_message():
    session = request.args.get("session")
    if not check_not_null(session):
        return "Ошибка: не указан номер сессии"
    filename = f"sessions/{str(session)}.json"
    return read_message(filename)


"""
Структура отправки сообщения:
session = номер сессии
user = отображаемое имя пользователя
msg = зашифрованное содержимое сообщения

Пример : http://127.0.0.1/message/new?session=0&user=Name&msg=Message
"""
@app.route("/message/new")  # Отправка сообщения
def new_message():
    # Получение аргументов из запроса
    session = request.args.get("session")
    user = request.args.get("user")
    msg = request.args.get("msg")

    if not check_not_null(session, user, msg):  # Если хотябы один элемент не указан, отмена сообщения
        return "Ошибка: параметры сообщения не указаны"

    session_status[int(session)] += 1  # Обновление сессии

    filename = f"sessions/{str(session)}.json"  # Получаем путь к файлу по номеру сессии
    write_message(filename, user, msg)  # Сохраняем сообщение
    print(f"{user} отправил сообщение, как пользователь {session}.")  # Лог
    return "Сообщение отправлено"


print("Сервер запущен с {}:{}".format(config["server_public_ip"], config["port"]))
app.run(debug=DEBUG, host=config["server_public_ip"], port=config["port"])
