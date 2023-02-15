import pandas as pd
from datetime import datetime, timedelta
import json


def open_file(file):
    with open(file, 'r', encoding='UTF-8') as f:
        data = json.load(f)
    return data

def get_tomorrow_shift(data:dict):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
    data = data['duty_queue']
    for key in data.keys():
        for value in data[key]:
            if value[0] == tomorrow:
                return key, value

def get_today_shift(data:dict):
    today = datetime.now().strftime("%d.%m.%Y")
    data = data['duty_queue']
    for key in data.keys():
        for value in data[key]:
            if value == today:
                return key, value


def get_week(data:dict):
    list = []
    today = datetime.now().strftime("%d.%m.%Y")
    data = data['duty_queue']
    for key in data.keys():
        for value in data[key]:
            list.append((key, value))

    return list

print(get_week(open_file('data.json')))

ts = pd.date_range(open_file('data.json')['duty_queue']['zarnii'][0][0], periods=1)
ts = pd.Series(ts).apply(str)
new = ts.str.split(" ", n=1, expand=True)
ts = new[0]
month = ts.apply(lambda x: int(x[5:7]))
mday = ts.apply(lambda x: int(x[8:10]))

# print(open_file('data.json')['duty_queue'])
# print(get_today_shift(open_file('data.json')))

def week_day(date):
    year, month, day = (int(x) for x in date.split('-'))
    answer = date(year, month, day).weekday()
    answer = int(answer) + 1
    return answer

