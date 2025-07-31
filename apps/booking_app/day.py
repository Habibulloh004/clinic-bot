from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)

from apps.analyze_app.logic.text import navigate_back_button
from apps.clinic_app.logic.endpoints import get_service_api
from apps.clinic_app.logic.states import BookingState, ClinicSelection
from apps.clinic_app.logic.text import (about_clinic_service_text,
                                        choice_time_text, no_dates_doctor_text,
                                        no_times_doctor_text)
from utils import get_language, t

router = Router()


@router.callback_query(StateFilter(BookingState.selecting_date),
                       F.data.startswith("date_"))
async def select_date(callback: CallbackQuery, state: FSMContext):
    """Выбор даты для записи к врачу"""
    lang = get_language(callback.from_user.id)

    date = callback.data.split("_")[1]
    data = await state.get_data()
    json_data = data.get('timetable_data')
    doctor_id = data.get('doctor_id')
    day, month, year = date.split('.')
    date = f'{year}-{month}-{day}'
    await state.update_data(selected_date=date)
    if not json_data or doctor_id not in json_data:
        return await callback.answer(t(no_dates_doctor_text, lang))

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
        InlineKeyboardButton(
            text=t(navigate_back_button, lang), callback_data="back_to_days")
    ])

    await callback.message.edit_text(t(choice_time_text, lang), parse_mode="HTML", reply_markup=keyboard)

    return await state.set_state(BookingState.selecting_time)


@router.callback_query(StateFilter(BookingState.selecting_date),
                       F.data == "back_to_doctors")
async def back_to_doctors(callback: CallbackQuery, state: FSMContext):
    """Возврат к выбору врачей"""
    lang = get_language(callback.from_user.id)

    data = await state.get_data()

    clinic_id, service_id = data.get('clinic_id'), data.get('service_id')
    services_data = get_service_api(clinic_id)

    await state.update_data(services=services_data)

    service_name, service_price = None, 0
    for service_tmp in services_data:
        if service_tmp.get("ServiceId") == int(service_id):
            service_name = service_tmp.get(
                "NameRu") if lang == "ru" else service_tmp.get("NameUz")
            service_price = service_tmp.get("Price")
            break

    clinic_name = data.get('clinic_name')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    doctors = data.get('doctors')
    if doctors:
        for doctor_id, name in doctors.items():
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text=name, callback_data=f'doctor_{doctor_id}')
            ])

    # Always add the "Назад" button at the end
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=t(navigate_back_button, lang),
                             callback_data="back_to_services")
    ])
    text = t(about_clinic_service_text, lang).format(
        clinic_name=clinic_name, service_name=service_name, service_price=service_price)
    print(service_name)
    await state.update_data(service_name=service_name)
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)

    await callback.answer()

    await state.set_state(ClinicSelection.selecting_doctor)
