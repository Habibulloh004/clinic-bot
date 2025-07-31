from aiogram.fsm.state import StatesGroup, State


class SearchClinic(StatesGroup):
    section = State()
    clinic = State()
    service = State()
    location = State()
