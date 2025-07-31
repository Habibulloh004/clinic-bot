from aiogram.fsm.state import State, StatesGroup


class ClinicSelection(StatesGroup):
    selecting_clinic = State()
    selecting_service = State()
    selecting_doctor = State()



class BookingState(StatesGroup):
    selecting_date = State()
    selecting_time = State()
    confirming_booking = State()
    booking_completed = State()
    booking_failed = State()
    commmenting = State()