from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.auth_app.logic.keyboards import menu_kb
from apps.buttons import back_button
from apps.settings_app.logic.states import SettingsState
from apps.settings_app.logic.text import settings_main_text
from utils import get_language, t

router = Router()


@router.message(SettingsState.field,
                lambda message: message.text in back_button.values())
async def qr_code(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    await message.answer(t(settings_main_text, lang), reply_markup=menu_kb(lang))
    await state.set_state(SettingsState.field)
