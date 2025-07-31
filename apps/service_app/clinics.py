from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from apps.auth_app.logic.keyboards import menu_kb
from apps.clinic_app.logic.states import ClinicSelection
from apps.clinic_app.logic.text import no_services_text, select_service_text
from apps.feedback_app.logic.text import backend_error_text
from apps.service_app.logic.states import SearchClinic
from utils import get_language, t

from ..texts import menu_text

router = Router()


@router.callback_query(StateFilter(SearchClinic.clinic),
                       F.data.startswith("clinic_"))
async def process_clinic_choice(callback: types.CallbackQuery, state: FSMContext):
    """ Choice of clinic and transition to service selection """
    lang = get_language(callback.from_user.id)
    clinic_id = callback.data.split("_")[1]
    clinic_name = callback.data.split("_")[2]

    await state.update_data(clinic_id=clinic_id, clinic_name=clinic_name)

    data = await state.get_data()
    section_id = data.get('section_id')
    message_id = data.get("message_id")
    try:
        await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=message_id)
    except Exception as e:
        print(e)
    from apps.clinic_app.logic.keyboards import services_kb
    print(clinic_id, section_id)
    keyboard = services_kb(clinic_id, lang, section_id=section_id)
    if not keyboard and keyboard is None:
        return await callback.answer(t(no_services_text, lang), reply_markup=menu_kb(lang))

    text = t(select_service_text, lang).format(clinic_name=clinic_name)
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)

    await callback.answer()

    return await state.set_state(ClinicSelection.selecting_service)


@router.callback_query(StateFilter(SearchClinic.clinic),
                       F.data.startswith("page_"))
async def paginate(callback: CallbackQuery, state: FSMContext):
    """Handles pagination of services."""
    lang = get_language(callback.from_user.id)
    page = int(callback.data.split("_")[1])

    user_data = await state.get_data()
    services = user_data.get("services", [])

    if not services:
        await callback.answer(t(backend_error_text, lang), show_alert=True)
        return await callback.message.answer(text=menu_text, reply_markup=menu_kb(lang))
    from apps.clinic_app.logic.keyboards import services_kb

    keyboard = services_kb(services, page=page)

    await callback.message.edit_reply_markup(reply_markup=keyboard)
    return await callback.answer()
