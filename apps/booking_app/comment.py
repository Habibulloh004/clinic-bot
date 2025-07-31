from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.auth_app.logic.keyboards import menu_kb
from apps.clinic_app.logic.endpoints import (add_reservation_api,
                                             create_notification_api,
                                             get_notification_templates_api)
from apps.clinic_app.logic.states import BookingState
from apps.clinic_app.logic.text import (booking_message_text,
                                        limit_booking_text, skip_button)
from apps.feedback_app.logic.text import backend_error_text
from db.query import get_datas_db
from utils import get_language, t

router = Router()


@router.message(StateFilter(BookingState.commmenting))
async def commenting_handler(message: Message, state: FSMContext):
    """Обработка комментария пользователя"""
    lang = get_language(message.from_user.id)
    if message.text == skip_button[lang]:
        comment = ''
    else:
        comment = message.text

    # Получаем данные из состояния
    data = await state.get_data()
    doctor_id = data.get('doctor_id')
    selected_date = data.get('selected_date')
    selected_time = data.get('selected_time')

    datas = await get_datas_db(message.from_user.id)
    status = add_reservation_api(
        user_name=datas.get('name'),
        birthday=datas.get('birthday'),
        gender=datas.get('gender'),
        phone=datas.get('phone_number'),
        come_date=selected_date + "T" + selected_time + ":00.000Z",
        clinic_id=data.get('clinic_id'),
        doctor_id=data.get('doctor_id'),
        service_id=data.get('service_id'),
        comment=comment
    )
    if status == 200:
        text = t(booking_message_text, lang).format(
            clinic_name=data.get('clinic_name'),
            service_name=data.get('service_name'),
            selected_date=selected_date,
            selected_time=selected_time
        )
        template_message = get_notification_templates_api()
        message_uz = template_message[0].get('message_uz')
        message_ru = template_message[0].get('message_ru')
        create_notification_api(
            clinic_id=data.get('clinic_id'),
            service_id=data.get('service_id'),
            doctor_id=data.get('doctor_id'),
            message_uz=message_uz.format(name=datas.get('name'), service_name=data.get('service_name'),
                                         phone=datas.get('phone_number')),
            message_ru=message_ru.format(name=datas.get('name'), service_name=data.get('service_name'),
                                         phone=datas.get('phone_number'))
        )

    elif status == 404:
        text = t(limit_booking_text, lang)
    else:
        text = backend_error_text[lang]
    await message.answer(text, reply_markup=menu_kb(lang))
    await state.clear()
