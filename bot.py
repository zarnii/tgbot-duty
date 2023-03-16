import logging
import asyncio
import aioschedule
from typing import List
from config import TOKEN, COMMANDS
from duty import make_duty, remake_duty
from dataclasses import dataclass, field
from json_queue import JsonInterface
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, executor
from dates import get_tomorrow_shift, get_today_shift, get_week
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


CHAT_ID = -936992816 #указать здесь свой айди, для отправкии сообщения в лс конкретному человеку


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
j = JsonInterface()

@dataclass
class Data:
	period_for_one_person: int
	queue: List[str] = field(default_factory=list)

	def __init__(self, period: int, queue: list):
		self.period_for_one_person = period
		self.queue = queue
		print(f'\n---Создан экземпляр класса Data---\nperiod_for_one_person - {self.period_for_one_person}\nqueue - {self.queue}')

Data = Data(j.get_period(), j.get_queue())


kb = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='Команды'),KeyboardButton(text='Узнать период'),KeyboardButton(text='Сегодня'), KeyboardButton(text='Завтра'), KeyboardButton(text='Неделя'), KeyboardButton(text='Для разработки')]
], resize_keyboard=True)

kbdev = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='Очистить absence'),KeyboardButton(text='Очистить duty_queue'),KeyboardButton(text='Назад')]
], resize_keyboard=True)

ikb = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='Да', callback_data='yes'), InlineKeyboardButton(text='Нет', callback_data='no')],
])


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
	await message.answer('Привет, я бот для создания рассписания', reply_markup=kb)


@dp.message_handler(commands=['set_period'])
async def set_period(message: types.Message):
	try:
		Data.period_for_one_person = int(message.get_args())
		j.set_period(int(message.get_args()))
		await message.answer(f'Установлен период дежурства для одного человека: {Data.period_for_one_person}')
	except ValueError:
		await message.reply('Введите число!')


@dp.message_handler(commands=['appoint'])
async def appoint_command(message: types.Message):
	if Data.period_for_one_person == 0:
		await message.reply('Сперва назначте период дежурства для одного человека!')
	else:
		if message.get_args() != '':
			Data.queue = message.get_args().split(' ')
			await message.reply(f'Задана очередь: {message.get_args()}\nВсе верно?', reply_markup = ikb)
		else: 
			await message.reply(f'Укажите дежурных')


@dp.message_handler(commands=['pass'])
async def create_pass(message: types.Message):
	if message.get_args() != '':
		pass_user = message.get_args().split(' ')
		if len(pass_user) != 2:
			await message.reply(f'Укажите человека и даты (пример: username 01.02.2023-05.02.2023)')
		else:
			if len(pass_user[1]) != 21:
				await message.reply(f'Укажите дату правильно! (пример: username 01.02.2023-05.02.2023)')
			else:
			#достаем дату из сообщения
				try:
					start = pass_user[1].split('-')[0]
					end = pass_user[1].split('-')[1]
					
					#преобразуем строку в дату
					start = datetime.strptime(start, '%d.%m.%Y')
					end = datetime.strptime(end, '%d.%m.%Y')

					#добовляем даты пропуска в массив
					pass_dates = []
					while start != end:
						pass_dates.append(str(start.strftime('%d.%m.%Y')))
						start += timedelta(days=1)

					#добовляем отсутвующего
					j.enabsence(pass_user[0], pass_dates)
					await message.reply(f'Операция была успешна проведена')
				except ValueError:
					await message.reply(f'Укажите дату правильно! (пример: username 01.02.2023-05.02.2023)')
	else:
		await message.reply(f'Укажите человека и даты (пример: username 01.02.2023-05.02.2023)')


@dp.callback_query_handler(text='yes')
async def confirm(callback: types.CallbackQuery):
	print(Data.queue, Data.period_for_one_person)
	j.clear_duty_queue()
	make_duty(Data.queue, Data.period_for_one_person, j)
	await callback.message.answer('Расписание составлено')
	await bot.send_message(CHAT_ID, f'Расписание составлено: {Data.queue}')

@dp.message_handler(commands=['add'])
async def add(message: types.Message):
	if len(message.get_args().split(' ')) != 1:
		await message.reply(f'Укажите nickname дежурного правильно!')
	else:
		Data.queue.append(message.get_args())
		j.clear_duty_queue()
		make_duty(Data.queue, Data.period_for_one_person, j)
		await message.answer('Дежурный был добавлен')
		await bot.send_message(CHAT_ID, f'Расписание было изменено: {Data.queue}')


@dp.message_handler(commands=['delete'])
async def delete_record(message: types.Message):
	delete_names = message.get_args().split(' ')
	print(f'Требуется удалить {delete_names}')

	search_name = delete_names[0]
	names = j.get_queue()
	id_ = 0
	for i in range(len(names)):
		if names[i] == search_name:
			id_ = i-1
			break

	for name in delete_names:
		j.dequeue(name)
		Data.queue.remove(name)
	print(f'---id_ = {id_}---')
	remake_duty(id_, j)
	await message.answer('Удаление было успешно произведено')
	await bot.send_message(CHAT_ID, f'Расписание было изменено: {Data.queue}')


@dp.message_handler(text='Команды')
async def command_btn_pressed(message: types.Message):
	await message.answer(COMMANDS)


@dp.message_handler(text='Для разработки')
async def dev_btn_pressed(message: types.Message):
	await message.answer('Клавиатура для разработки', reply_markup=kbdev)


@dp.message_handler(text='Очистить absence')
async def clra_btn_pressed(message: types.Message):
	j.clear_absence()


@dp.message_handler(text='Очистить duty_queue')
async def clrd_btn_pressed(message: types.Message):
	j.clear_duty_queue()


@dp.message_handler(text='Назад')
async def back_btn_pressed(message: types.Message):
	await message.answer('Назад', reply_markup=kb)


@dp.message_handler(text='Узнать период')
async def period_btn_pressed(message: types.Message):
	await message.answer(f'Заданный период: {Data.period_for_one_person}')



@dp.message_handler(text='Сегодня')
async def today(message: types.Message):
	text = get_today_shift(j.cout_duty_queue())
	if text == None:
		await message.answer('Сегодня дежурных нет')
	else:
		await message.answer(text)


@dp.message_handler(text='Завтра')
async def tomorrow(message: types.Message):
	text = get_tomorrow_shift(j.cout_duty_queue())
	if text == None:
		await message.answer('Завтра дежурных нет')
	else:
		await message.answer(text)


@dp.message_handler(text='Неделя')
async def tomorrow(message: types.Message):
	text = get_week(j.cout_duty_queue())
	await message.answer(text)


@dp.message_handler(text='Назад')
async def tomorrow(message: types.Message):
	await message.delete()
	await message.answer('Назад', reply_markup=kb)


@dp.message_handler()
async def appoint_command(message: types.Message):
	await message.reply('Нет такой команды')
	print(message)


async def send_mess():
	duty_person = get_today_shift(j.cout_duty_queue())
	await bot.send_message(CHAT_ID, f"Сегодня дежурит: @{duty_person}")


async def scheduler():
	aioschedule.every().day.at("13:45").do(send_mess)
	while True:
		await aioschedule.run_pending()
		await asyncio.sleep(1)


async def on_startup(dp):
	asyncio.create_task(scheduler())


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
