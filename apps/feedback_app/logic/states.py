from aiogram.fsm.state import State, StatesGroup


class FeedBackState(StatesGroup):
    text = State()
    feedback_rate = State()

    choice = State()
    list = State()