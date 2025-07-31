from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from apps.auth_app.logic.keyboards import menu_kb
from apps.clinic_app.logic.endpoints import get_clinics_api
from apps.clinic_app.logic.keyboards import clinics_kb, services_kb
from apps.clinic_app.logic.states import ClinicSelection
from apps.clinic_app.logic.text import no_services_text, select_service_text, no_clinics_text
from apps.feedback_app.logic.text import backend_error_text
from utils import get_language, t

router = Router()


@router.callback_query(
    StateFilter(ClinicSelection.selecting_clinic),
    F.data.startswith("clinic_")
)
async def select_clinic(callback: CallbackQuery, state: FSMContext):
    """ Choice of clinic and transition to service selection """
    lang = get_language(callback.from_user.id)
    clinic_id = callback.data.split("_")[1]
    clinic_name = callback.data.split("_")[2]

    await state.update_data(clinic_id=clinic_id)
    await state.update_data(clinic_name=clinic_name)

    data = await state.get_data()
    message_id = data.get("message_id")
    try:
        await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=message_id)
    except Exception as e:
        print(e)
    keyboard = services_kb(clinic_id, lang)
    if not keyboard and keyboard is None:
        return await callback.answer(t(no_services_text, lang), reply_markup=menu_kb(lang))

    text = t(select_service_text, lang).format(clinic_name=clinic_name)
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)

    await callback.answer()

    return await state.set_state(ClinicSelection.selecting_service)


@router.callback_query(
    StateFilter(ClinicSelection.selecting_clinic),
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
