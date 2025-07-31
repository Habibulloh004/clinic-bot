from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.auth_app.logic.keyboards import menu_kb
from apps.buttons import back_button, menu_services_button
from apps.feedback_app.logic.text import backend_error_text
from apps.service_app.logic.endpoints import get_sections_endpoint
from apps.service_app.logic.keyboards import sections_kb
from apps.service_app.logic.states import SearchClinic
from apps.service_app.logic.texts import (no_service_text, select_service_text,
                                          send_location_text)
from apps.texts import menu_text
from utils import get_language, t

router = Router()


@router.message(lambda message: message.text in menu_services_button.values())
async def doctor_handler(message: types.Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    sections = get_sections_endpoint()

    if not sections:
        return await message.answer(t(no_service_text, lang))
    if sections is None:
        return await message.answer(t(backend_error_text, lang))

    await state.update_data(sections=sections)

    keyboard = sections_kb(sections, lang=lang, page=0)

    await message.answer(t(select_service_text, lang), reply_markup=keyboard)
    return await state.set_state(SearchClinic.section)


@router.message(SearchClinic.clinic)
async def back_handler(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    if message.text == back_button[lang]:
        await state.clear()
    return await message.answer(t(menu_text, lang), reply_markup=menu_kb(lang))


@router.message(SearchClinic.location)
async def handle_invalid_location_input(message: Message, state: FSMContext):
    """Handles invalid location input and prompts the user to send their location."""
    lang = get_language(message.from_user.id)
    if message.text in back_button[lang]:
        await state.clear()
        return await message.answer(t(menu_text, lang), reply_markup=menu_kb(lang))

    return await message.answer(t(send_location_text, lang))
