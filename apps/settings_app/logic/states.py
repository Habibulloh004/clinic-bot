from aiogram.fsm.state import State, StatesGroup


class SettingsState(StatesGroup):
    field = State()

    name = State()
    phone = State()
    age = State()
    language = State() 
    notification = State()