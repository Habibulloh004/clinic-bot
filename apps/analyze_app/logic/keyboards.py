from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from apps.analyze_app.logic.text import navigate_back_button, navigate_next_button
from utils import t


def create_pdf_kb(data_list, page: int = 0, page_size: int = 5, lang: str = 'ru') -> InlineKeyboardMarkup:
    start = page * page_size
    end = start + page_size
    chunk = data_list[start:end]

    keyboard = []

    for item in chunk:
        button = InlineKeyboardButton(
            text=f"{item['result']['clinic_name']} ({item['result']['visitDate']})",
            callback_data=f"analyze_{item['id']}"
        )
        keyboard.append([button])

    navigation_buttons = []

    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(text=t(navigate_back_button, lang), callback_data=f"page_{page - 1}")
        )
    if end < len(data_list):
        navigation_buttons.append(
            InlineKeyboardButton(text=t(navigate_next_button, lang), callback_data=f"page_{page + 1}")
        )

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
