import json
from datetime import datetime
duty_queue = {}
k = 1


def show_duty_persons():
    return len(all_dutyers)


def make_schedule():
    global k
    for j in range(show_duty_persons()): # проход по всем дежурным
        for i in range(2): # период дежурничесива
            if all_dutyers[j] not in duty_queue:
                duty_queue[all_dutyers[j]] = [f'{get_now_day() + k}.{get_now_month()}.{get_now_year()}']
            else:
                duty_queue[all_dutyers[j]] += [f'{get_now_day() + k}.{get_now_month()}.{get_now_year()}']
            k += 1
    print(duty_queue) # {'zarnii': ['3.2.2023', '4.2.2023'], 'krakazyabra2102': ['5.2.2023', '6.2.2023']}


def get_now_day() -> int:
    now_day = int(datetime.now().strftime('%d'))
    return now_day


def get_now_month() -> int:
    now_month = int(datetime.now().strftime('%m'))
    return now_month


def get_now_year() -> int:
    now_year = int(datetime.now().strftime('%Y'))
    return now_year


def get_date_of():
    pass


with open('data.json', 'r', encoding='utf-8') as f:  #
    text = json.load(f)
    all_lists = list(text)
    all_dutyers = list(text[all_lists[0]])
    make_schedule()