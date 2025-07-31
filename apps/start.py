from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.auth_app.logic.keyboards import language_kb, menu_kb
from apps.auth_app.logic.states import Register
from apps.texts import choice_language_text, menu_text
from utils import get_language, t

router = Router()


@router.message(Command("start"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(choice_language_text, reply_markup=language_kb())
    await state.set_state(Register.lang)


@router.message(StateFilter('*'), Command("restart"))
async def command_restart_handler(message: Message, state: FSMContext) -> None:
    lang = get_language(message.from_user.id)
    await state.clear()
    await message.answer(t(menu_text, lang), reply_markup=menu_kb(lang))
