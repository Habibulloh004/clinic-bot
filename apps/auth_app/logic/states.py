from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    lang = State()
    name = State()
    gender = State()
    phone = State()
    birthday = State()
