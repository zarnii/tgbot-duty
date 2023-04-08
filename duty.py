from datetime import datetime, timedelta
from json_queue import JsonInterface


def make_duty(names: list, period: int, q: JsonInterface, k: int = 1) -> None:
	for name in names:
		q.enqueue(name, [])
		if name not in q.get_absence():
			q.enabsence(name, [])
	dates_for_next = []
	k = 1
	holidays = q.get_holidays()
	absence = q.get_absence_dict()
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

if __name__ == "__main__":
	j = JsonInterface()
	remake_duty(0, j)