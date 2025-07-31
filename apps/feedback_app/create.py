from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from apps.analyze_app.logic.endpoints import get_pdf_by_phone_api
from apps.auth_app.logic.keyboards import menu_kb
from apps.feedback_app.logic.endpoints import add_remark_api
from apps.feedback_app.logic.keyboards import feedback_kb, score_kb
from apps.feedback_app.logic.states import FeedBackState
from apps.feedback_app.logic.text import (backend_error_text,
                                          data_not_found_text,
                                          feedback_post_button, feedback_text,
                                          feedback_thanks_text,
                                          no_visited_clinics_text,
                                          score_less_3_text, score_text,
                                          write_comment_text)
from apps.settings_app.logic.keyboards import back_kb
from utils import get_language, t

router = Router()


@router.message(StateFilter(FeedBackState.choice),
                lambda message: message.text in feedback_post_button.values())
async def feedback_create(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    lang = get_language(telegram_id)
    data = await get_pdf_by_phone_api(telegram_id)

    if data is None:
        return await message.answer(t(backend_error_text, lang), reply_markup=menu_kb(lang))

    if not data:
        return await message.answer(t(no_visited_clinics_text, lang), reply_markup=menu_kb(lang))

    await state.update_data(json_data=data)

    await message.answer(t(write_comment_text, lang), reply_markup=back_kb(lang))

    await message.answer(t(feedback_text, lang),
                         reply_markup=feedback_kb(data, page=0, lang=lang))
    return await state.set_state(FeedBackState.feedback_rate)


@router.callback_query(StateFilter(FeedBackState.feedback_rate),
                       F.data.startswith("feedback_"))
async def send_pdf_by_id(callback_query: types.CallbackQuery, state: FSMContext):
    lang = get_language(callback_query.from_user.id)
    analyze_id = int(callback_query.data.split("_")[1])

    data = await state.get_data()
    data = data.get("json_data", [])
    await state.update_data(analyze_id=analyze_id)
    clinic = next(
        (item for item in data if item['result']['clinic_id'] == analyze_id), None)
    clinic = clinic.get("result")

    keyboard = score_kb()

    await callback_query.message.delete()
    text = t(score_text, lang).format(
        clinic_name=clinic.get('clinic_name', ''),
        branch=clinic.get('branch', ''),
        visit_date=clinic.get('visitDate', '')
    )

    await callback_query.message.answer(text, reply_markup=keyboard)


@router.callback_query(StateFilter(FeedBackState.feedback_rate),
                       F.data.startswith("page_"))
async def paginate(callback_query: CallbackQuery, state: FSMContext):
    lang = get_language(callback_query.from_user.id)
    page = int(callback_query.data.split("_")[1])

    user_data = await state.get_data()
    data = user_data.get("json_data", [])

    if not data:
        return await callback_query.answer(t(data_not_found_text, lang), show_alert=True)

    return await callback_query.message.edit_reply_markup(reply_markup=feedback_kb(data, page=page, lang=lang))


@router.callback_query(F.data.startswith("rate_"))
async def handle_rating(callback_query: types.CallbackQuery, state: FSMContext):
    lang = get_language(callback_query.from_user.id)
    rating = int(callback_query.data.split("_")[1])

    data = await state.get_data()
    await state.update_data(rating=rating)
    await callback_query.message.delete()
    if rating <= 3:
        await callback_query.message.answer(t(score_less_3_text, lang),
                                            reply_markup=types.ReplyKeyboardRemove())
        return await state.set_state(FeedBackState.text)

    else:
        response = add_remark_api(
            service_id=data.get('analyze_id'), score=rating)

    if response is None:
        return await callback_query.answer(t(backend_error_text, lang),
                                           reply_markup=menu_kb(lang))

    await state.clear()
    return await callback_query.message.answer(t(feedback_thanks_text, lang), reply_markup=menu_kb(lang))
