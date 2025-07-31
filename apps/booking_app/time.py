from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup)

from apps.analyze_app.logic.text import navigate_back_button
from apps.buttons import back_button
from apps.clinic_app.logic.states import BookingState, ClinicSelection
from apps.clinic_app.logic.text import (choice_day_text, choice_time_text,
                                        comment_booking_text,
                                        confirm_booking_text, confirm_button,
                                        confirmed_booking_text,
                                        doctor_busy_text, no_dates_doctor_text,
                                        no_times_doctor_text, skip_button)
from utils import get_language, t

router = Router()


@router.callback_query(
    StateFilter(BookingState.selecting_time),
    F.data.startswith('time_'))
async def select_time(callback: CallbackQuery, state: FSMContext):
    """Выбор времени для записи к врачу"""
    lang = get_language(callback.from_user.id)

    time = callback.data.split('_')[1]
    await state.update_data(selected_time=time)
    data = await state.get_data()
    doctor_id = data.get('doctor_id')
    json_data = data.get('timetable_data')
    date = data.get('selected_date')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t(confirm_button, lang),
                                 callback_data="confirm_booking")
        ],
        [
            InlineKeyboardButton(text=t(back_button, lang),
                                 callback_data="back_to_times")
        ]
    ])

    text = t(confirm_booking_text, lang).format(date=date, time=time)

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)
    await state.set_state(BookingState.selecting_time)


@router.callback_query(
    StateFilter(BookingState.selecting_time),
    F.data == 'confirm_booking')
async def confirm_booking(callback: CallbackQuery, state: FSMContext):
    """Подтверждение записи и запрос комментария"""
    # Удаляем предыдущее сообщение

    lang = get_language(callback.from_user.id)
    data = await state.get_data()
    text = t(confirmed_booking_text, lang).format(selected_date=data.get('selected_date'),
                                                  selected_time=data.get('selected_time'))
    await callback.message.edit_text(text, parse_mode="HTML")

    # Клавиатура с кнопкой "Пропустить"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(skip_button, lang))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    # Отправляем сообщение
    await callback.message.answer(t(comment_booking_text, lang), reply_markup=keyboard)
    await state.set_state(BookingState.commmenting)


@router.callback_query(StateFilter(BookingState.selecting_time),
                       F.data == 'back_to_times')
async def back_to_times(callback: CallbackQuery, state: FSMContext):
    """Возврат к выбору времени"""
    lang = get_language(callback.from_user.id)

    data = await state.get_data()
    doctor_id = data.get('doctor_id')
    json_data = data.get('timetable_data')

    if not json_data or doctor_id not in json_data:
        return await callback.answer(t(no_dates_doctor_text, lang))

    date = data.get('selected_date')
    times = json_data[doctor_id].get(date, [])

    if not times:
        return await callback.answer(t(no_times_doctor_text, lang))

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    row = []
    for i, time in enumerate(times, 1):
        time_text = time.get('slot_time')[:5]
        row.append(InlineKeyboardButton(text=time_text,
                                        callback_data=f'time_{time_text}'))
        if i % 5 == 0:
            keyboard.inline_keyboard.append(row)
            row = []
    if row:
        keyboard.inline_keyboard.append(row)

    # Add the "Back" button as its own row
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=t(navigate_back_button, lang),
                             callback_data="back_to_days")
    ])

    await callback.message.edit_text(t(choice_time_text, lang),
                                     parse_mode="HTML",
                                     reply_markup=keyboard
                                     )
    return await state.set_state(BookingState.selecting_time)


@router.callback_query(
    StateFilter(BookingState.selecting_time),
    F.data == 'back_to_days'
)
async def select_time_back(callback: CallbackQuery, state: FSMContext):
    lang = get_language(callback.from_user.id)

    data = await state.get_data()

    doctor_id = data.get('doctor_id')
    json_data = data.get('timetable_data')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    dates = json_data.get(doctor_id).keys()
    if dates:
        for name in dates:
            year, month, day = name.split('-')
            name = f"{day}.{month}.{year}"
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text=name, callback_data=f'date_{name}')
            ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=t(back_button, lang),
                             callback_data="back_to_doctors")
    ])
    if len(keyboard.inline_keyboard) == 1:
        text = t(doctor_busy_text, lang)
        await state.set_state(ClinicSelection.selecting_service)
    else:
        text = t(choice_day_text, lang)
        await state.set_state(BookingState.selecting_date)
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=keyboard
    )
