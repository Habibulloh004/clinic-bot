from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.buttons import back_button
from apps.settings_app.logic.keyboards import back_kb, settings_kb
from apps.settings_app.logic.states import SettingsState
from apps.settings_app.logic.text import *
from utils import get_language, t

router = Router()


@router.message(SettingsState.field, lambda message: message.text in settings_update_age_button.values())
async def name_start(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    await message.answer(t(ask_age_text, lang), reply_markup=back_kb(lang))
    await state.set_state(SettingsState.age)


@router.message(SettingsState.age)
async def name_handler(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    if message.text == back_button[lang]:
        await state.set_state(SettingsState.field)
        return await message.answer(t(settings_main_text, lang),
                                    reply_markup=settings_kb(lang))
    else:
        if not message.text.isdigit():
            await state.set_state(SettingsState.age)
            return await message.answer(t(invalid_type_age, lang))
        age = int(message.text)
        if age < 0 or age > 120:
            await state.set_state(SettingsState.age)
            return await message.answer(t(invalid_max_age, lang))

        await message.answer(t(success_age_text, lang), reply_markup=settings_kb(lang))
        await state.set_state(SettingsState.field)
        return None
