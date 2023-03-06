import logging
from typing import List
from config import TOKEN
from duty import make_duty
from dataclasses import dataclass, field
from json_queue import JsonInterface
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import aioschedule
import asyncio

us_id = 123456789 # указать здесь свой айди, для отправкии сообщения в лс конкретному человеку


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dataclass
class Data:
	period_for_one_person: int = 0
	queue: List[str] = field(default_factory=list)
Data = Data()

kb = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='Команды'),KeyboardButton(text='Узнать период'),KeyboardButton(text='Узнать расписание')]
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
			#await make_duty(queue, period_for_one_person)
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
		j = JsonInterface()
		j.enabsence(pass_user[0], pass_dates)
	else:
		await message.reply(f'Укажите человека и даты (пример: @username 01.02.2023-05.02.2023)')


@dp.callback_query_handler(text='yes')
async def confirm(callback: types.CallbackQuery):
	await make_duty(Data.queue, Data.period_for_one_person)
	await callback.message.answer('Расписание составлено')


@dp.message_handler(commands=['delete'])
async def delete_record(message: types.Message):
	j = JsonInterface()
	users = message.get_args()
	for i in users:
		j.dequeue(i)



@dp.message_handler(text='Команды')
async def command_btn_pressed(message: types.Message):
	await message.answer('/set_period - команда для установки периода дежуртсва для одного человека\n/appoint - создание списка дежурства')


@dp.message_handler(text='Узнать период')
async def period_btn_pressed(message: types.Message):
	await message.answer(f'Заданный период: {Data.period_for_one_person}')


@dp.message_handler(text='Узнать расписание')
async def duty_btn_pressed(message: types.Message):
	await message.answer(f'Список дежурных: {Data.queue}')


@dp.message_handler()
async def appoint_command(message: types.Message):
	await message.reply('Нет такой команды')

	
async def send_mess():
    await bot.send_message(us_id, "Сегодня дежурит: *такой-то*")


async def scheduler():
    aioschedule.every().day.at("9:00").do(send_mess)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    asyncio.create_task(scheduler())

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
