from datetime import datetime, timedelta
from json_queue import JsonInterface


async def make_duty(names: list, period: int, q: JsonInterface, k: int = 1) -> None:
	for name in names:
		q.enqueue(name, [])
		q.enabsence(name, [])
	dates_for_next = []
	holidays = q.get_holidays()
	absence = q.cout_absence()
	for name in names:
		dates = []
		for days in dates_for_next:
			dates.append(days)
		#print(dates)
		dates_for_next = []
		# for j in range(period - len(dates)):
		while len(dates) < period:
			date = (datetime.now() + timedelta(days=k)).strftime("%d.%m")
			date_miss = (datetime.now() + timedelta(days=k)).strftime("%d.%m.%Y")

			date_add = (datetime.now() + timedelta(days=k)).strftime("%d.%m.%Y")
			if date not in holidays:
				if date_miss not in absence[name]:
					k += 1
					dates.append(date_add)
				else:
					k += 1
					dates_for_next.append(date_miss)
			else:
				k += 1
		q.enqueue(name, dates)


def remake_duty(id_:int, j: JsonInterface):
	'''
	-в def передается никнейм человека(id_) с которого надо пересоставить расписание(никнейм человека после которого был удален человек)
	-в переменную start помешяется последняя дата дежуртсва id_ в формате datetime
	-затем получаем список людей для которых нужно пересоставить расписание(remake_duty_name)
	-пересоставляем расписание по принципу работы make_duty
	'''
	q = j.cout_duty_queue()
	name = list(q.keys())[id_]
	start = datetime.strptime(q[name][j.get_period()-1], '%d.%m.%Y')


if __name__ == "__main__":
	j = JsonInterface()
	remake_duty(0, j)