from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram import Bot, Dispatcher, types, executor
from datetime import datetime, timedelta
from json_queue import JsonInterface
from duty import make_duty
from config import TOKEN
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


period_for_one_person = 0
queue = []

kb = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='Команды'),KeyboardButton(text='Узнать период'),KeyboardButton(text='Узнать расписание')]
], resize_keyboard=True)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
	await message.answer('Привет, я бот для создания рассписания', reply_markup=kb)


@dp.message_handler(commands=['set_period'])
async def set_period(message: types.Message):
	try:
		global period_for_one_person
		period_for_one_person = int(message.get_args())
		await message.answer(f'Установлен период дежурства для одного человека: {period_for_one_person}')
	except ValueError:
		await message.reply('Введите число!')


@dp.message_handler(commands=['appoint'])
async def appoint_command(message: types.Message):
	if period_for_one_person == 0:
		await message.reply('Сперва назначте период дежурства для одного человека!')
	else:
		if message.get_args() != '':
			queue = message.get_args().split(' ')
			await message.reply(f'Задана очередь: {message.get_args()}')
			await make_duty(queue, period_for_one_person)
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
		q = JsonInterface()
		q.enabsence(pass_user[0], pass_dates)
	else:
		await message.reply(f'Укажите человека и даты (пример: @username 01.02.2023-05.02.2023)')




@dp.message_handler(text='Команды')
async def command_btn_pressed(message: types.Message):
	await message.answer('/set_period - команда для установки периода дежуртсва для одного человека\n/appoint - создание списка дежурства')


@dp.message_handler(text='Узнать период')
async def period_btn_pressed(message: types.Message):
	await message.answer(f'Заданный период: {period_for_one_person}')


@dp.message_handler(text='Узнать расписание')
async def duty_btn_pressed(message: types.Message):
	await message.answer(f'Список дежурных: {queue}')


@dp.message_handler()
async def appoint_command(message: types.Message):
	await message.reply('Нет такой команды')


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)