import aiohttp
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message

from apps.auth_app.logic.keyboards import menu_kb
from apps.buttons import menu_pdf_button
from apps.feedback_app.logic.text import backend_error_text
from utils import datetime_converter, get_language, t

from .logic.endpoints import get_pdf_by_phone_api
from .logic.keyboards import create_pdf_kb
from .logic.states import Analyze
from .logic.text import no_result_pdf_text, pdf_not_found_text, pdf_text

router = Router()


@router.message(lambda message: message.text in menu_pdf_button.values())
async def feedback_start(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    lang = get_language(telegram_id)

    data = await get_pdf_by_phone_api(telegram_id)

    if data is None:
        return await message.answer(t(backend_error_text, lang), reply_markup=menu_kb(lang))

    if not data:
        return await message.answer(t(no_result_pdf_text, lang), reply_markup=menu_kb(lang))

    await state.update_data(json_data=data)

    await message.answer(t(pdf_text, lang), reply_markup=create_pdf_kb(data, page=0, lang=lang))

    return await state.set_state(Analyze.analyze)


@router.callback_query(StateFilter(Analyze.analyze),
                       F.data.startswith("analyze_"))
async def send_pdf_by_id(callback_query: CallbackQuery, state: FSMContext):
    lang = get_language(callback_query.from_user.id)
    analyze_id = int(callback_query.data.split("_")[1])

    user_data = await state.get_data()
    data = user_data.get("json_data", [])

    doc = next((item for item in data if item['id'] == analyze_id), None)

    await callback_query.message.delete()
    if doc:
        file_url = doc["path"]
        file_name = f"{doc.get('result', {}).get('clinic_name')}_{datetime_converter(doc.get('result', {}).get('visitDate'))}.pdf"

        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as resp:
                if resp.status == 200:
                    file_bytes = await resp.read()

        # Отправляем файл из памяти
        await callback_query.message.answer_document(
            BufferedInputFile(file_bytes, filename=file_name)
        )
    else:
        await callback_query.message.answer(t(pdf_not_found_text, lang))

    await callback_query.answer()


@router.callback_query(StateFilter(Analyze.analyze),
                       F.data.startswith("page_"))
async def paginate(callback_query: CallbackQuery, state: FSMContext):
    lang = get_language(callback_query.from_user.id)
    page = int(callback_query.data.split("_")[1])

    user_data = await state.get_data()
    data = user_data.get("json_data", [])

    if not data:
        return await callback_query.answer(t(backend_error_text, lang), show_alert=True, reply_markup=menu_kb(lang))

    await callback_query.message.edit_reply_markup(reply_markup=create_pdf_kb(data, page=page, lang=lang))

    await callback_query.answer()
    return await state.set_state(Analyze.analyze)
