from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.auth_app.logic.keyboards import lang_map, language_kb
from apps.auth_app.logic.text import invalid_language_text
from apps.buttons import back_button
from apps.settings_app.logic.keyboards import settings_kb
from apps.settings_app.logic.states import SettingsState
from apps.settings_app.logic.text import (change_language_text,
                                          settings_language_button,
                                          settings_main_text,
                                          success_language_text)
from middleware import LanguageMiddleware
from utils import get_language, t

router = Router()


@router.message(
    SettingsState.field,
    lambda message: message.text in settings_language_button.values()
)
async def name_start(message: Message, state: FSMContext) -> None:
    telegram_id = message.from_user.id
    lang = get_language(telegram_id)

    await message.answer(
        t(change_language_text, lang),
        reply_markup=language_kb()
    )
    await state.set_state(SettingsState.language)


@router.message(SettingsState.language)
async def lang_handler(message: Message, state: FSMContext):
    lang = lang_map.get(message.text)

    if not lang:
        await state.set_state(SettingsState.language)
        return await message.answer(t(invalid_language_text, lang))

    elif message.text == back_button[lang]:
        await state.set_state(SettingsState.field)
        return await message.answer(t(settings_main_text, lang),
                                    reply_markup=settings_kb(lang))

    else:
        LanguageMiddleware.set_language(message.from_user.id, lang)
        lang = lang_map.get(message.text)

        await message.answer(
            t(success_language_text, lang),
            reply_markup=settings_kb(lang)
        )

        return await state.set_state(SettingsState.field)
