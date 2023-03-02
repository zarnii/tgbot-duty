from datetime import datetime, timedelta
from json_queue import JsonInterface


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
					mensaje += "На завтра не назначен дежурный"

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
					mensaje += "На завтра не назначен дежурный"
				return mensaje 


def get_week(data: dict):
	date_worker = []
	today = datetime.now().strftime("%d.%m.%Y")

	for key in data:
		for value in data[key]:
			date_worker.append((key, value))
	message = ''
	for i,val in enumerate(date_worker):
		if val[1] == today:
			for idx, val in enumerate(date_worker, start=i):
				if idx == 7:
					break
				else:
					message += f"{val[1]}, дежурит {val[0]}\n"

	return message

def get_period_vis(data: dict, start: str, end: str):
	date_worker = []
	for key in data:
		for value in data[key]:
			date_worker.append((key,value))
	message = ''
	if start not in date_worker or end not in date_worker:
		message += "Дата начала/конца выходит за рамки расписания"
		return message
	for i, val in enumerate(date_worker):
		if val[1] == start:
			for idx, val in enumerate(date_worker, start=i):
				if val[1] == end:
					break
				else:
					message += f"{val[1]}, дежурит {val[0]}\n"
	return message

if __name__ == '__main__':
	queue = JsonInterface().cout_duty_queue()
	print(get_tomorrow_shift(queue))