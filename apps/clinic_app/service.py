from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)

from apps.auth_app.logic.keyboards import menu_kb
from apps.buttons import back_button
from apps.clinic_app.logic.endpoints import (get_reservation_timetable_api,
                                             get_service_api)
from apps.clinic_app.logic.keyboards import clinics_kb, services_kb
from apps.clinic_app.logic.states import ClinicSelection
from apps.clinic_app.logic.text import (about_clinic_service_text,
                                        booking_text, no_clinics_text,
                                        no_doctor_text, select_clinic_text)
from apps.feedback_app.logic.text import backend_error_text
from apps.service_app.logic.states import SearchClinic
from utils import get_language, t

router = Router()


@router.callback_query(StateFilter(ClinicSelection.selecting_service),
                       F.data.startswith("service_"))
async def select_service(callback: CallbackQuery, state: FSMContext):
    lang = get_language(callback.from_user.id)

    tmp, clinic_id, service_id = callback.data.split("_")
    services_data = get_service_api(clinic_id)

    doctors, data_json = get_reservation_timetable_api(
        int(clinic_id), int(service_id), lang)

    await state.update_data(
        clinic_id=clinic_id,
        service_id=service_id,
        services=services_data,
        doctors=doctors,
        timetable_data=data_json
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    if doctors:
        for doctor_id, name in doctors.items():
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text=name, callback_data=f'doctor_{doctor_id}')
            ])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=t(back_button, lang),
                             callback_data="back_to_services")
    ])

    data = await state.get_data()

    service_name, service_price = None, 0
    for service_tmp in services_data:
        if service_tmp.get("ServiceId") == int(service_id):
            service_name = service_tmp.get(
                "NameRu") if lang == "ru" else service_tmp.get("NameUz")
            service_price = service_tmp.get("Price")
            break

    clinic_name = data.get('clinic_name')
    text = t(about_clinic_service_text, lang).format(
        clinic_name=clinic_name, service_name=service_name, service_price=service_price)
    await callback.message.edit_text(text, parse_mode="HTML")
    await state.update_data(service_name=service_name)
    text = t(booking_text, lang)
    if not doctors:
        text = t(no_doctor_text, lang)
    await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()

    await state.set_state(ClinicSelection.selecting_doctor)


@router.callback_query(StateFilter(ClinicSelection.selecting_service),
                       F.data.startswith("page_"))
async def clinics_pagination(callback: CallbackQuery, state: FSMContext):
    """ Start pagination for clinics """
    page = int(callback.data.split("_")[1])
    lang = get_language(callback.from_user.id)
    user_data = await state.get_data()
    section_id = user_data.get('section_id')
    data = user_data.get('clinic_id')
    await callback.message.edit_reply_markup(
        reply_markup=services_kb(data, page=page, lang=lang, section_id=section_id))
    await callback.answer()


@router.callback_query(StateFilter(ClinicSelection.selecting_service),
                       F.data == "back_to_clinics")
async def back_to_clinics(callback: CallbackQuery, state: FSMContext):
    lang = get_language(callback.from_user.id)
    data = await state.get_data()
    print("data: ", data)

    # clinics = get_clinics_api()
    clinics = data.get('clinics')
    if clinics is None:
        return await callback.message.answer(t(backend_error_text, lang), reply_markup=menu_kb(lang))
    if not clinics:
        return await callback.message.answer(t(no_clinics_text, lang),
                                             reply_markup=menu_kb(lang))
    await callback.message.edit_text(t(select_clinic_text, lang), reply_markup=clinics_kb(clinics=clinics))
    await callback.answer()
    print(data.get('section_id'))
    if data.get('section_id'):
        return await state.set_state(SearchClinic.clinic)
    else:
        return await state.set_state(ClinicSelection.selecting_clinic)
