from flask import Flask, request
import json
import logging

with open("config.json", "r", encoding = 'utf-8') as config_file:
    config = json.loads(config_file.read())

app = Flask("EnigmaIRC Server")

app.logger.disabled = config["disable_request_logs"]
log = logging.getLogger("werkzeug")
log.disabled = config["disable_request_logs"]

session_status = []
for i in range(config["session_count"]):
    session_status.append(0)


@app.route("/")
def main():
    return config


@app.route("/message/new")
def newMessage():
    session = request.args.get("session")
    user = request.args.get("user")
    msg = request.args.get("msg")

    session_status[int(session)] += 1

    filename = f"sessions/{str(session)}.json"
    writeMessage(filename, user, msg)
    print(f"{user} sent message, using session {session}.")
    return "Message was sent successfully"


@app.route("/message/get")
def getMessage():
    session = request.args.get("session")
    filename = f"sessions/{str(session)}.json"
    return readMessage(filename)


@app.route("/sessions")
def getSessions():
    return session_status


def writeMessage(file, user, msg):
    message_data = {
        "user": user,
        "msg": msg
    }
    with open(file, "w", encoding = "utf-8") as msg_file:
        msg_file.write(json.dumps(message_data))


def readMessage(file):
    with open(file, "r", encoding = "utf-8") as msg_file:
        message = json.loads(msg_file.read())
    return message


print("Server was started on {}:{}".format(config["server_public_ip"], config["port"]))
app.run(debug = False, host = config["server_public_ip"], port = config["port"])
