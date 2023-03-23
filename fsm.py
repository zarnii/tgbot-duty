from aiogram.dispatcher.filters.state import State, StatesGroup


class BotStates(StatesGroup):
	SET_PERIOD_STATE = State()
	APPOINT_STATE = State()
	PASS_STATE = State()
	DELETE_STATE = State()
	ADD_STATE = State()
