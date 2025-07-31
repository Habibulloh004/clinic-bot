from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup

from apps.auth_app.logic.keyboards import menu_kb
from apps.buttons import menu_clinic_button
from apps.clinic_app.logic.endpoints import get_clinics_api
from apps.clinic_app.logic.keyboards import clinics_kb
from apps.clinic_app.logic.states import ClinicSelection
from apps.clinic_app.logic.text import (no_clinics_text, select_clinic_text,
                                        write_clinic_name_text)
from apps.feedback_app.logic.text import backend_error_text
from utils import get_language, t

router = Router()


@router.message(lambda message: message.text in menu_clinic_button.values())
async def start_clinic_selection(message: types.Message, state: FSMContext):
    """ Start clinic selection process """
    lang = get_language(message.from_user.id)
    clinics = get_clinics_api()
    await state.update_data(clinics=clinics)
    if clinics is None:
        return await message.answer(t(backend_error_text, lang), reply_markup=menu_kb(lang))

    if not clinics:
        return await message.answer(t(no_clinics_text, lang), reply_markup=menu_kb(lang))

    keyboards = clinics_kb(clinics=clinics, lang=lang)

    await message.answer(t(select_clinic_text, lang), reply_markup=keyboards)

    msg = await message.answer(
        t(write_clinic_name_text, lang),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[],
            resize_keyboard=True,
            input_field_placeholder="Enter clinic name..."
        ),
    )

    await state.update_data(message_id=msg.message_id)
    return await state.set_state(ClinicSelection.selecting_clinic)
