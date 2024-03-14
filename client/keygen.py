from utils.config import *
import utils.setup as setup

with open("config.json", "r", encoding = 'utf-8') as config_file:
    config = json.loads(config_file.read())

if config["isFirstLaunch"]:
    setup.setup()

from cryptography.fernet import Fernet

print("Your key is ", Fernet.generate_key())
input()