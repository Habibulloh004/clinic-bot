from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.auth_app.logic.keyboards import menu_kb
from apps.buttons import back_button, menu_feedback_button
from apps.feedback_app.logic.endpoints import add_remark_api
from apps.feedback_app.logic.keyboards import choice_feedback_kb
from apps.feedback_app.logic.states import FeedBackState
from apps.feedback_app.logic.text import (backend_error_text,
                                          choice_feedback_text,
                                          feedback_thanks_text)
from apps.texts import menu_text
from db.query import get_phone_number_db
from utils import get_language, t

router = Router()


@router.message(F.text.in_(menu_feedback_button.values()))
async def feedback_start(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    lang = get_language(telegram_id)
    keyboard = choice_feedback_kb(lang)
    await message.answer(t(choice_feedback_text, lang), reply_markup=keyboard)
    await state.set_state(FeedBackState.choice)


@router.message(FeedBackState.text)
async def feedback_text_handler(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    phone_number = await get_phone_number_db(message.from_user.id)
    if message.text == t(back_button, lang):
        await state.clear()
        return await message.answer(t(menu_text, lang), reply_markup=menu_kb(lang))

    data = await state.get_data()
    response = add_remark_api(service_id=data.get(
        'analyze_id'), score=data.get('rating'), comment=message.text + "\nPhone: " + phone_number)

    if response is None:
        return await message.answer(t(backend_error_text, lang), reply_markup=menu_kb(lang))

    await state.clear()

    return await message.answer(t(feedback_thanks_text, lang), reply_markup=menu_kb(lang))
