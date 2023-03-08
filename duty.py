from datetime import datetime, timedelta
from json_queue import JsonInterface


def make_duty(names: list, period: int, q: JsonInterface, k: int = 1) -> None:
	for name in names:
		q.enqueue(name, [])
		q.enabsence(name, [])
	dates_for_next = []
	k = 1
	holidays = q.get_holidays()
	absence = q.get_absence()
	for name in names:
		dates = []
		for days in dates_for_next:
			dates.append(days)
		print(dates)
		dates_for_next = []
		# for j in range(period - len(dates)):
		while len(dates) < period:
			date = (datetime.now() + timedelta(days=k)).strftime("%d.%m")
			check_week = (datetime.now() + timedelta(days=k)).strftime("%A")
			date_miss = (datetime.now() + timedelta(days=k)).strftime("%d.%m.%Y")

			date_add = (datetime.now() + timedelta(days=k)).strftime("%d.%m.%Y")
			if date not in holidays and (check_week not in ('Saturday', 'Sunday')):
				if date_miss not in absence[name]:
					k += 1
					dates.append(date_add)
				else:
					k += 1
					dates_for_next.append(date_miss)
			else:
				k += 1
		q.enqueue(name, dates)


def remake_duty(id_:int, j: JsonInterface) -> None:
	#я не знаю как оно работает
	q = j.cout_duty_queue()
	
	if id_ >= 0:
		name = list(q.keys())[id_]
		start = datetime.strptime(q[name][j.get_period()-1], '%d.%m.%Y')

		id_ += 1
		period = j.get_period()
		while id_ < len(q):
			name = list(q.keys())[id_]
			arr = []
			for i in range(period):
				start += timedelta(days=1)
				if start.weekday() == 5:
					start += timedelta(days=2)
				elif start.weekday() == 6:
					start += timedelta(days=1)
				arr.append(start.strftime("%d.%m.%Y"))
			q[name] = arr
			id_ += 1
			print(f'Для {name} - {arr}')
		print(f'---НОВОЕ РАСПИСАНИЕ---\n{q}')
		j.set_all_queue(q)
	elif id_ < 0:
		id_ = 0 
		name = list(q.keys())[id_]
		start = datetime.now()
		period = j.get_period()

		while id_ < len(q):
			name = list(q.keys())[id_]
			arr = []
			for i in range(period):
				start += timedelta(days=1)
				if start.weekday() == 5:
					start += timedelta(days=2)
				elif start.weekday() == 6:
					start += timedelta(days=1)
				arr.append(start.strftime("%d.%m.%Y"))
			q[name] = arr
			id_ += 1
			print(f'Для {name} - {arr}')
		print(f'---НОВОЕ РАСПИСАНИЕ---\n{q}')
		j.set_all_queue(q)


if __name__ == "__main__":
	j = JsonInterface()
	remake_duty(0, j)