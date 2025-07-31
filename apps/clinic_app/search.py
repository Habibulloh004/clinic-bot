from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from apps.auth_app.logic.keyboards import menu_kb
from apps.clinic_app.logic.endpoints import get_clinic_services_by_name_api
from apps.clinic_app.logic.keyboards import clinics_kb
from apps.clinic_app.logic.states import ClinicSelection
from apps.clinic_app.logic.text import (invalid_input_clinic_name,
                                        no_clinics_text, select_clinic_text)
from apps.feedback_app.logic.text import backend_error_text
from utils import get_language, t

router = Router()


@router.message(ClinicSelection.selecting_clinic)
async def handle_clinic_selection(message: types.Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    clinic_name = message.text.strip()

    # Check if the user is trying to search for a clinic by name
    if len(clinic_name) < 3:
        return await message.answer(t(invalid_input_clinic_name, lang))

    # Check if the user is trying to select a clinic from the list
    clinics = get_clinic_services_by_name_api(clinic_name)
    if clinics is None:
        await state.clear()
        return await message.answer(t(backend_error_text, lang), reply_markup=menu_kb(lang))

    if not clinics:
        await state.clear()
        return await message.answer(t(no_clinics_text, lang), reply_markup=menu_kb(lang))

    keyboards = clinics_kb(clinics=clinics, lang=lang)
    if not keyboards or keyboards is None:
        await state.clear()
        return await message.answer(t(no_clinics_text, lang), reply_markup=menu_kb(lang))

    await message.answer(t(select_clinic_text, lang), reply_markup=keyboards)

    return await state.set_state(ClinicSelection.selecting_clinic)
