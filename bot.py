import logging
from typing import List
from config import TOKEN, COMMANDS
from duty import make_duty, remake_duty
from dataclasses import dataclass, field
from json_queue import JsonInterface
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, executor
from dates import get_tomorrow_shift, get_today_shift, get_week
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


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
	[KeyboardButton(text='Команды'),KeyboardButton(text='Узнать период'),KeyboardButton(text='Клавиатура рассписания')]
], resize_keyboard=True)

kbdate = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='Сегодня'), KeyboardButton(text='Завтра'), KeyboardButton(text='Неделя'), KeyboardButton(text='Назад')]
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

		#достаем дату из сообщения
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
	else:
		await message.reply(f'Укажите человека и даты (пример: username 01.02.2023-05.02.2023)')


@dp.callback_query_handler(text='yes')
async def confirm(callback: types.CallbackQuery):
	print(Data.queue, Data.period_for_one_person)
	j.clear_duty_queue()
	await make_duty(Data.queue, Data.period_for_one_person, j)
	await callback.message.answer('Расписание составлено')


@dp.message_handler(commands=['delete'])
async def delete_record(message: types.Message):
	names = message.get_args().split(' ')
	print(f'Требуется удалить {names}')
	for name in names:
		j.dequeue(name)
		Data.queue.remove(name)
	await callback.message.answer('Удаление было успешно произведено')


@dp.message_handler(text='Команды')
async def command_btn_pressed(message: types.Message):
	await message.answer(COMMANDS)


@dp.message_handler(text='Узнать период')
async def period_btn_pressed(message: types.Message):
	await message.answer(f'Заданный период: {Data.period_for_one_person}')


@dp.message_handler(text='Клавиатура рассписания')
async def duty_btn_pressed(message: types.Message):
	await message.answer('Выберите', reply_markup = kbdate)


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


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
