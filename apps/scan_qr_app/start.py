import os

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from apps.auth_app.logic.keyboards import menu_kb
from apps.buttons import menu_qr_button
from apps.scan_qr_app.logic.text import first_phone_number_text, scan_qr_text
from apps.scan_qr_app.qr_code import generate_phone_qr
from db.query import get_phone_number_db
from utils import get_language, t

router = Router()


@router.message(lambda message: message.text in menu_qr_button.values())
async def send_qr_code(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    phone_number = await get_phone_number_db(message.from_user.id)
    if not phone_number:
        return await message.answer(t(first_phone_number_text, lang))

    file_path = f"{phone_number}.png"
    generate_phone_qr(phone_number, filename=file_path)

    await message.answer_photo(FSInputFile(file_path), caption=t(scan_qr_text, lang), reply_markup=menu_kb(lang))

    # Delete the QR code image after sending
    if os.path.exists(file_path):
        os.remove(file_path)
    return None
