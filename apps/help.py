from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.auth_app.logic.keyboards import menu_kb
from apps.buttons import back_button
from apps.texts import help_message, menu_text
from utils import get_language, t

router = Router()


@router.message(Command("help"))
async def command_help_handler(message: Message, state: FSMContext) -> None:
    lang = get_language(message.from_user.id)
    await state.clear()
    await message.answer(t(help_message, lang), reply_markup=menu_kb(lang), parse_mode='HTML')


@router.message(lambda message: message.text in back_button.values())
async def back_handler(message: types.Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    await state.clear()
    await message.answer(t(menu_text, lang), reply_markup=menu_kb(lang))
