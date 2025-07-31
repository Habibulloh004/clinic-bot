from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.settings_app.logic.keyboards import (settings_kb)
from apps.settings_app.logic.states import SettingsState
from apps.settings_app.logic.text import settings_notifications_button, ask_notification_text
from utils import get_language, t

router = Router()


@router.message(SettingsState.field, lambda message: message.text in settings_notifications_button.values())
async def name_start(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    await message.answer(t(ask_notification_text, lang), reply_markup=settings_kb(lang))
    await state.set_state(SettingsState.field)
