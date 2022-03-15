from aiogram.dispatcher.filters.state import State, StatesGroup


class FindState(StatesGroup):
    wait_game = State()
