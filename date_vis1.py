from datetime import datetime, timedelta
from json_queue import JsonInterface

queue = JsonInterface().cout_duty_queue()


def get_tomorrow_shift(data: dict):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
    mensaje = ''  # сообщение
    for key in data:
        for value in data[key]:
            if value == tomorrow:
                try:
                    mensaje += f"Завтра {value}, дежурит {key} "
                except TypeError as error:
                    print(error)
                    mensaje += "На сегодня не назначен дежурный"

                return mensaje


def get_today_shift(data: dict):
    today = datetime.now().strftime("%d.%m.%Y")
    mensaje = ''
    for key in data:
        for value in data[key]:
            if value == today:
                try:
                    mensaje += f"Сегодня {value}, дежурит {key}"
                except TypeError as error:
                    print(error)
                    mensaje += "На сегодня не назначен дежурный"
                return mensaje


def get_week(data: dict):
    date_n_worker = []

    for key in data:
        for value in data[key]:
            date_n_worker.append((key, value))

    message = ''
    for idx, val in enumerate(date_n_worker):
        if idx == 7:
            break
        else:
            message += f"Сегодня {val[1]}, дежурит {val[0]}\n"

    return message
