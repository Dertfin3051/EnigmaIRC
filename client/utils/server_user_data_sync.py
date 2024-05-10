from colorama import Fore


def get_session(server_config) -> int:
    """
    Получение номера сессии от пользователя с учётом проверок и исключений
    """
    max_sessions = server_config["session_count"] - 1
    while True:
        try:
            session = int(input(f"Номер сессии(от 0 до {max_sessions}): "))  # Номер сессии
            if not (session >= 0 and session <= max_sessions):  # Пользователь ввёл неверный номер
                print(Fore.RED + "Вы ввели некорректный номер сессии!\n" + Fore.RESET)
            else:
                return session
        except ValueError:  # Пользователь ввёл не число
            print(Fore.RED + "Вы ввели некорректный номер сессии!\n" + Fore.RESET)

def try_server_connection(server_url: str):
    try:
        import requests
        requests.get(server_url)
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "Не удаётся подключиться к серверу. Возможно, вы забыли указать данный параметр!")
        input()
        exit(0)
