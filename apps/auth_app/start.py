from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from apps.buttons import gender_female_button, gender_male_button
from db.query import save_user_db
from middleware import LanguageMiddleware
from utils import get_language, t

from .logic.keyboards import gender_kb, lang_map, menu_kb, phone_number_kb
from .logic.states import Register
from .logic.text import *
from .logic.utils import validate_name, validate_phone_number

router = Router()


@router.message(Register.lang)
async def handle_language(message: Message, state: FSMContext):
    lang = lang_map.get(message.text)
    telegram_id = message.from_user.id

    if not lang:
        return await message.answer(t(invalid_language_text, lang))

    LanguageMiddleware.set_language(telegram_id, lang)

    await message.answer(t(auth_language_text, lang), reply_markup=ReplyKeyboardRemove())
    return await state.set_state(Register.name)


@router.message(Register.name)
async def handle_name(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    name = message.text.strip()

    if validate_name(name):
        await state.update_data(name=name)
        await message.answer(t(auth_name_text, lang), reply_markup=gender_kb(lang))
        await state.set_state(Register.gender)
    else:
        await message.answer(t(invalid_name_text, lang), reply_markup=ReplyKeyboardRemove())


@router.message(Register.gender)
async def handle_gender(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)
    gender = message.text.strip()

    if not ((gender == gender_male_button[lang]) or (gender == gender_female_button[lang])):
        return await message.answer(t(invalid_gender_text, lang), reply_markup=gender_kb(lang))

    await state.update_data(gender=1 if gender == gender_male_button[lang] else 0)
    await message.answer(t(auth_gender_text, lang), reply_markup=phone_number_kb(lang))
    return await state.set_state(Register.phone)


@router.message(Register.phone)
async def handle_phone(message: Message, state: FSMContext):
    lang = get_language(message.from_user.id)

    if message.contact:
        contact_number = message.contact.phone_number
        if not contact_number.startswith("+"):
            contact_number = "+" + contact_number
    else:
        contact_number = message.text.strip()

    validated_number = validate_phone_number(contact_number)

    if not validated_number:
        return await message.answer(t(invalid_phone_text, lang))

    await state.update_data(phone_number=contact_number)

    await message.answer(t(auth_phone_text, lang), reply_markup=ReplyKeyboardRemove())
    return await state.set_state(Register.birthday)


@router.message(Register.birthday)
async def handle_birthday(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    lang = get_language(telegram_id)
    birthday = message.text.strip()

    # Validate format DD-MM-YYYY
    try:
        datetime.strptime(birthday, "%d-%m-%Y")
    except ValueError:
        return await message.answer(
            t(invalid_birthday_text, lang)
        )

    await state.update_data(birthday=birthday)

    user_data = await state.get_data()

    await save_user_db(
        telegram_id=telegram_id,
        phone_number=user_data.get("phone_number"),
        birthday=user_data.get("birthday"),
        language=lang,
        name=user_data.get("name"),
        gender=user_data.get("gender")
    )

    await state.clear()
    return await message.answer(t(auth_birthday_text, lang), reply_markup=menu_kb(lang))
