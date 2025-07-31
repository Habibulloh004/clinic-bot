from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)

from apps.analyze_app.logic.text import navigate_back_button
from apps.clinic_app.logic.keyboards import services_kb
from apps.clinic_app.logic.states import BookingState, ClinicSelection
from apps.clinic_app.logic.text import (choice_day_text, doctor_busy_text,
                                        select_service_text)
from utils import get_language, t

router = Router()


@router.callback_query(StateFilter(ClinicSelection.selecting_doctor),
                       F.data.startswith("doctor_"))
async def doctor_booking(callback: CallbackQuery, state: FSMContext):
    lang = get_language(callback.from_user.id)

    doctor_id = callback.data.split("_")[1]
    data = await state.get_data()
    await state.update_data(doctor_id=doctor_id)
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
        InlineKeyboardButton(text=t(navigate_back_button, lang),
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


@router.callback_query(StateFilter(ClinicSelection.selecting_doctor),
                       F.data == "back_to_services")
async def back_to_services(callback: CallbackQuery, state: FSMContext):
    """Возврат к выбору услуг"""
    lang = get_language(callback.from_user.id)
    data = await state.get_data()
    clinic_id = data["clinic_id"]
    clinic_name = data.get('clinic_name')

    text = t(select_service_text, lang).format(clinic_name=clinic_name)

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=services_kb(clinic_id, lang))
    await callback.answer()
    return await state.set_state(ClinicSelection.selecting_service)
