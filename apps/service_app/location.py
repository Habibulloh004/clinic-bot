from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.auth_app.logic.keyboards import menu_kb
from apps.feedback_app.logic.text import backend_error_text
from apps.service_app.logic.endpoints import post_get_clinics_nearby_endpoint
from apps.service_app.logic.keyboards import clinics_keyboard
from apps.service_app.logic.states import SearchClinic
from apps.service_app.logic.texts import (near_clinics_text,
                                          no_near_clinics_text,
                                          select_clinic_text)
from utils import get_language, t

router = Router()


@router.message(SearchClinic.location, F.location)
async def handle_location(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    user_location = message.location
    user_data = await state.get_data()
    section_id = user_data.get('section_id')

    latitude, longitude = user_location.latitude, user_location.longitude
    # Fetch the list of clinics
    clinics = post_get_clinics_nearby_endpoint(
        lat=latitude, lon=longitude, section_id=section_id, lang=lang
    )
    if clinics is None:
        return await message.answer(t(backend_error_text, lang), reply_markup=menu_kb(lang))
    if not clinics:
        return await message.answer(t(no_near_clinics_text, lang), reply_markup=menu_kb(lang))

    # Save clinics data into state
    await state.update_data(clinics=clinics)
    # Create the keyboard with clinics
    keyboards = clinics_keyboard(clinics, page=0, lang=lang)

    await message.answer(t(near_clinics_text, lang), reply_markup=menu_kb(lang))
    await message.answer(t(select_clinic_text, lang), reply_markup=keyboards)
    return await state.set_state(SearchClinic.clinic)
