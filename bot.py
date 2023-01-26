from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


period_for_one_person = 0

kb = ReplyKeyboardMarkup(keyboard=[
	[KeyboardButton(text='Команды', callback_data='commands_btn'),KeyboardButton(text='Узнать период', callback_data='period_btn'),KeyboardButton(text='Узнать расписание', callback_data='duty_btn')]
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
		await message.reply(f'Задана очередь: {message.get_args()}')


'''
@dp.callback_query_handler(text='commands_btn')
async def ...

@dp.callback_query_handler(text='period_btn')
async def ...

@dp.callback_query_handler(text='duty_btn')
async def ...
'''

@dp.message_handler()
async def appoint_command(message: types.Message):
	await message.reply('Нет такой команды')


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)