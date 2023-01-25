from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

period_for_one_person = 0

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
	await message.answer('Привет, я бот для создания рассписания')



@dp.message_handler(commands=['set_period'])
async def set_period(message: types.Message):
	try:
		period_for_one_person = int(message.get_args())
		await message.answer(f'Установлен период дежурства для одного человека: {period_for_one_person}')
	except ValueError:
		await message.reply('Введите число!')


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)