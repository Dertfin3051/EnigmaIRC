from flask import Flask, request
import logging

from handlers import check_not_null, write_message, read_message, get_config, generate_empty_sessions

app = Flask("EnigmaIRC Server")  # Создаём приложение
DEBUG = False

config = get_config()

# Отключение авто-логов
app.logger.disabled = config["disable_request_logs"]
log = logging.getLogger("werkzeug")
log.disabled = config["disable_request_logs"]

session_status = generate_empty_sessions()  # Важная переменная. Хранит актуальное кол-во отправленных сообщений. Если у клиента сообщений меньше, чем на сервере, то срабатывает триггер на получение нового сообщения


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
