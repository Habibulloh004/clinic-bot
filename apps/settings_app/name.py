from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.auth_app.logic.text import (invalid_name_text, invalid_name_type,
                                      success_name_text)
from apps.buttons import back_button
from apps.settings_app.logic.keyboards import back_kb, settings_kb
from apps.settings_app.logic.states import SettingsState
from apps.settings_app.logic.text import (ask_name_text,
                                          settings_change_name_button)
from apps.texts import menu_text
from utils import get_language, t

router = Router()


@router.message(SettingsState.field,
                lambda message: message.text in settings_change_name_button.values())
async def name_start(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)

    await message.answer(t(ask_name_text, lang), reply_markup=back_kb(lang))
    await state.set_state(SettingsState.name)


@router.message(SettingsState.name)
async def name_handler(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)

    if message.text == back_button[lang]:
        await message.answer(t(menu_text, lang), reply_markup=settings_kb(lang))

    else:
        name = message.text
        if len(name) < 2 or len(name) > 50:
            await state.set_state(SettingsState.name)
            return await message.answer(t(invalid_name_text, lang))
        if not name.isalpha():
            await state.set_state(SettingsState.name)
            return await message.answer(t(invalid_name_type, lang))

        await state.update_data(name=name)
        return await message.answer(t(success_name_text, lang), reply_markup=settings_kb(lang))

    return await state.set_state(SettingsState.field)
