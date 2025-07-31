from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from apps.auth_app.logic.keyboards import menu_kb
from apps.feedback_app.logic.text import backend_error_text
from apps.service_app.logic.keyboards import location_kb, sections_kb
from apps.service_app.logic.states import SearchClinic
from apps.service_app.logic.texts import send_location_text
from apps.texts import menu_text
from utils import get_language, t

router = Router()


@router.callback_query(StateFilter(SearchClinic.section), F.data.startswith("section_"))
async def process_service(callback: CallbackQuery, state: FSMContext):
    """Processes the selected service and prompts for location."""
    lang = get_language(callback.from_user.id)

    section_id = callback.data.split('_')[1]
    section_name = callback.data.split('_')[2]
    await state.update_data(section_id=section_id, section_name=section_name)

    keyboards = location_kb(lang)
    await callback.message.delete()
    await callback.message.answer(t(send_location_text, lang), reply_markup=keyboards)
    await state.set_state(SearchClinic.location)


@router.callback_query(StateFilter(SearchClinic.section),
                       F.data.startswith("page_"))
async def paginate(callback: CallbackQuery, state: FSMContext):
    """Handles pagination of services."""
    lang = get_language(callback.from_user.id)
    page = int(callback.data.split("_")[1])

    user_data = await state.get_data()
    sections = user_data.get("sections", [])

    if not sections:
        await callback.answer(t(backend_error_text, lang), show_alert=True)
        return await callback.message.answer(text=t(menu_text, lang), reply_markup=menu_kb(lang))
    else:
        keyboard = sections_kb(sections, page=page)
        await callback.message.edit_reply_markup(reply_markup=keyboard)
        return await callback.answer()
