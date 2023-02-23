import json

class JsonInterface:
	def __init__(self):
		#открывается файл для создания очереди
		with open('data.json', 'r', encoding='UTF-8') as f:
			self.data = json.load(f)

			self.duty_queue = self.data["duty_queue"]
			self.absence = self.data["absence"]

			self.queue = []
			for i in self.duty_queue:
				self.queue.append(i)


	def get_queue(self) -> list:
		return self.queue

	def get_period(self) -> int:
		return self.data["duty_period"]


	def get_holidays(self) -> list:
		return self.data["holidays"]
	

	def get_absence(self) -> list:
		return self.data["absence"]


	#вынимание первого из очереди
	def dequeue(self, name) -> None:
		if len(self.queue) < 1:
			return None
		else:
			#удаление из json файла и из списка queue
			self.duty_queue.pop(name)
			self.queue.remove(name)

			#перезапись json файла
			with open('data.json', 'w', encoding="UTF-8") as f:
				f.write(json.dumps(self.data))


	#добавление в очередь
	def enqueue(self, nickname: str, date: list) -> None:
		self.duty_queue[nickname] = date
		self.queue.append(nickname)

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
		if len(self.queue) < 1:
			return True
		else:
			return False


	#делает duty_queue пустым
	def clear_duty_queue(self) -> None:
		self.duty_queue.clear()
		with open('data.json', 'w', encoding="UTF-8") as f:
			f.write(json.dumps(self.data))

	#создание словоря дежурных
	def cout_duty_queue(self) -> dict:
		d = {}

		for i in self.duty_queue:
			d[i] = self.duty_queue[i]

		return d

	#создание словоря отсутвующих
	def cout_absence(self) -> dict:
		d = {}

		for i in self.absence:
			d[i] = self.absence[i]

		return d

if __name__ == '__main__':
	j = JsonInterface()
	j.create_empty()