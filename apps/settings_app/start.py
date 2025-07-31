from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.buttons import menu_settings_button
from apps.settings_app.logic.keyboards import settings_kb
from apps.settings_app.logic.states import SettingsState
from apps.settings_app.logic.text import settings_main_text
from utils import get_language, t

router = Router()


@router.message(lambda message: message.text in menu_settings_button.values())
async def settings_handler(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    await message.answer(t(settings_main_text, lang), reply_markup=settings_kb(lang))
    await state.set_state(SettingsState.field)
