import os
from .config import *


def setup():
    print("Установка дополнений...")
    os.system("pip install -r requirements.txt")    # Установка библиотек из списка
    config = getConfig()    # Чтение конфига
    config["isFirstLaunch"] = False    # Отключение установки для последующих запусков
    saveConfig(config)    # Сохранение
    import colorama
    colorama.init()
    colorama.just_fix_windows_console()
    print(colorama.Fore.LIGHTGREEN_EX + "Все необходимые дополнения успешно установлены" + colorama.Fore.RESET)

if __name__ == '__main__':
    setup()
    input()
