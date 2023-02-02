import json

class Queue:
	def __init__(self):
		#открывается файл для создания очереди
		with open('data.json', 'r', encoding='UTF-8') as f:
			self.data = json.load(f)

			self.duty_queue = self.data["duty_queue"]
			self.absence = self.data["absence"]

			self.queue = [] 
			for i in self.duty_queue:
				self.queue.append(i)


	#вынимание первого из очереди
	def dequeue(self):
		if len(self.queue) < 1:
			return None
		else:
			#удаление из json файла и из списка queue
			self.duty_queue.pop(self.queue[0])
			self.queue.pop(0)

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
	def empty(self):
		if len(self.queue) < 1:
			return True
		else:
			return False

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
