from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    Counter = State()
    Calculator = State()
    First_date = State()
    Second_date = State()
