from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from apps.auth_app.logic.keyboards import menu_kb
from apps.clinic_app.logic.endpoints import get_clinics_api
from apps.clinic_app.logic.keyboards import clinics_kb
from apps.clinic_app.logic.text import no_clinics_text, select_clinic_text
from apps.feedback_app.logic.endpoints import list_remark_by_clinic_id_api
from apps.feedback_app.logic.keyboards import choice_feedback_kb
from apps.feedback_app.logic.states import FeedBackState
from apps.feedback_app.logic.text import (backend_error_text, feedback_labels,
                                          feedback_list_button,
                                          invalid_data_clinic,
                                          no_feedback_text)
from utils import get_language, t

router = Router()


@router.message(StateFilter(FeedBackState.choice),
                lambda message: message.text in feedback_list_button.values())
async def feedback_create(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    lang = get_language(telegram_id)
    clinics = get_clinics_api()
    await state.update_data(clinics=clinics)
    if clinics is None:
        return await message.answer(t(backend_error_text, lang), reply_markup=menu_kb(lang))

    if not clinics:
        return await message.answer(t(no_clinics_text, lang), reply_markup=menu_kb(lang))

    keyboards = clinics_kb(clinics=clinics, lang=lang)

    await message.answer(t(select_clinic_text, lang), reply_markup=keyboards)

    return await state.set_state(FeedBackState.list)


@router.callback_query(
    StateFilter(FeedBackState.list),
    F.data.startswith("clinic_")
)
async def select_clinic(callback: CallbackQuery, state: FSMContext):
    """Handle clinic selection and display its feedback"""
    user_id = callback.from_user.id
    lang = get_language(user_id)

    # Extract clinic ID and name from callback data
    try:
        _, clinic_id, clinic_name = callback.data.split("_", 2)
    except ValueError:
        await callback.answer(t(invalid_data_clinic, lang), show_alert=True)
        return

    # Fetch feedback data from the API
    feedback_data = list_remark_by_clinic_id_api(clinic_id)

    # Remove the previous message
    await callback.message.delete()

    if not feedback_data or not feedback_data.get("scoresList"):
        await callback.message.answer(t(no_feedback_text, lang))
        return await state.set_state(FeedBackState.choice)

    scores = feedback_data["scoresList"]

    labels = feedback_labels.get(lang, feedback_labels["ru"])

    # Format the feedback
    formatted_feedback = "\n\n".join([
        f"{labels['score']}: {item['score']}/5\n"
        f"{labels['comment']}: {item['comment'] or labels['no_comment']}\n"
        f"{labels['date']}: {item['created_time'].split('T')[0]}"
        for item in scores
    ])

    # Send feedback to the user
    await callback.message.answer(
        labels["title"].format(clinic=clinic_name) +
        '\n\n' + formatted_feedback,
        parse_mode="Markdown",
        reply_markup=choice_feedback_kb(lang)
    )

    return await state.set_state(FeedBackState.choice)


@router.callback_query(
    StateFilter(FeedBackState.list),
    F.data.startswith("page_")
)
async def clinics_pagination(callback: CallbackQuery, state: FSMContext):
    """ Start pagination for clinics """
    lang = get_language(callback.from_user.id)
    page = int(callback.data.split("_")[1])

    clinics = get_clinics_api()
    if clinics is None:
        return await callback.message.answer(t(backend_error_text, lang), reply_markup=menu_kb(lang))

    if not clinics:
        return await callback.message.answer(t(no_clinics_text, lang), reply_markup=menu_kb(lang))

    await callback.message.edit_reply_markup(reply_markup=clinics_kb(clinics=clinics, page=page, lang=lang))
    return await callback.answer()
