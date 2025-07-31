from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.auth_app.logic.text import invalid_phone_text, success_phone_text
from apps.auth_app.logic.utils import validate_phone_number
from apps.buttons import back_button
from apps.settings_app.logic.keyboards import back_kb, settings_kb
from apps.settings_app.logic.states import SettingsState
from apps.settings_app.logic.text import (ask_phone_text, settings_main_text,
                                          settings_phone_button)
from utils import get_language, t

router = Router()


@router.message(
    SettingsState.field,
    lambda message: message.text in settings_phone_button.values()
)
async def name_start(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    await message.answer(t(ask_phone_text, lang), reply_markup=back_kb(lang))
    await state.set_state(SettingsState.phone)


@router.message(SettingsState.phone)
async def name_handler(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)

    if message.text in back_button[lang]:
        await state.set_state(SettingsState.field)
        return await message.answer(t(settings_main_text, lang),
                                    reply_markup=settings_kb(lang))

    else:
        if message.contact:
            contact_number = message.contact.phone_number

            if not contact_number.startswith("+"):
                contact_number = "+" + contact_number

        contact_number = message.text.strip()

        validated_number = validate_phone_number(contact_number)

        if not validated_number:
            await state.set_state(SettingsState.phone)
            return await message.answer(t(invalid_phone_text, lang))

        await message.answer(text=t(success_phone_text, lang), reply_markup=settings_kb(lang))
        return await state.set_state(SettingsState.field)
