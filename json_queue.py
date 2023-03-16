import json

class JsonInterface:
	def __init__(self):
		#открывается файл для создания очереди
		with open('data.json', 'r', encoding='UTF-8') as f:
			self.data = json.load(f)

			self.duty_queue = self.data["duty_queue"]
			self.absence = self.data["absence"]
			print(f'\n---Создан экземпляр класса JsonInterface---\nduty_queue - {self.duty_queue}\nabsence - {self.absence}')

	def get_queue(self) -> list:
		return list(self.duty_queue.keys())

	def get_period(self) -> int:
		return self.data["duty_period"]


	def get_holidays(self) -> list:
		return self.data["holidays"]
	

	def get_absence(self) -> list:
		return list(self.absence.keys())


	def set_period(self, period: int) -> None:
		self.data["duty_period"] = period

		with open('data.json', 'w', encoding="UTF-8") as f:
				f.write(json.dumps(self.data))

	def set_all_queue(self, new):
		self.data["duty_queue"] = new

		with open('data.json', 'w', encoding="UTF-8") as f:
				f.write(json.dumps(self.data))


	#вынимание очереди
	def dequeue(self, name) -> None:
		if len(list(self.duty_queue.keys())) < 1:
			return None
		else:
			#удаление из json файла и из списка queue
			print(f'\n---РАБОТАЕТ dequeue---\nудаляется {name}')
			self.duty_queue.pop(name)

			#перезапись json файла
			with open('data.json', 'w', encoding="UTF-8") as f:
				f.write(json.dumps(self.data))


	#добавление в очередь
	def enqueue(self, nickname: str, date: list) -> None:
		print(f'\n---РАБОТАЕТ enqueue---\nдобавялется {nickname} с датой {date}')
		self.duty_queue[nickname] = date

		#перезапись json файла
		with open('data.json', 'w', encoding="UTF-8") as f:
			f.write(json.dumps(self.data))


	#добавление отсутвующих
	def enabsence(self, nickname: str, date: list) -> None:
		self.absence[nickname] = date

		with open('data.json', 'w', encoding="UTF-8") as f:
			f.write(json.dumps(self.data))


	#проверка на пустоту
	def empty(self) -> bool:
		if len(list(self.duty_queue.keys())) < 1:
			return True
		else:
			return False


	#делает duty_queue пустым
	def clear_duty_queue(self) -> None:
		self.duty_queue.clear()
		with open('data.json', 'w', encoding="UTF-8") as f:
			f.write(json.dumps(self.data))

	def clear_absence(self) -> None:
		self.absence.clear()
		with open('data.json', 'w', encoding="UTF-8") as f:
			f.write(json.dumps(self.data))

	#создание словоря дежурных
	def cout_duty_queue(self) -> dict:
		d = {}

		for i in self.duty_queue:
			d[i] = self.duty_queue[i]

		return d

	#создание словоря отсутвующих
	def get_absence_dict(self) -> dict:
		return self.data["absence"]

if __name__ == '__main__':
	j = JsonInterface()
	j.create_empty()