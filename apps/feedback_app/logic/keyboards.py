from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from apps.buttons import back_button, next_button_text
from apps.feedback_app.logic.text import feedback_list_button, feedback_post_button
from utils import t


def feedback_kb(data_list, page: int = 0, page_size: int = 5, lang: str = 'ru'):
    start = page * page_size
    end = start + page_size
    chunk = data_list[start:end]

    keyboard = []

    for item in chunk:
        button = InlineKeyboardButton(
            text=f"{item['result']['clinic_name']} ({item['result']['visitDate']})",
            callback_data=f"feedback_{item['result']['clinic_id']}"
        )
        keyboard.append([button])

    navigation_buttons = []

    if page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(
                text=t(back_button, lang), callback_data=f"page_{page - 1}"
            )
        )
    if end < len(data_list):
        navigation_buttons.append(
            InlineKeyboardButton(
                text=t(next_button_text, lang), callback_data=f"page_{page + 1}"
            )
        )

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def choice_feedback_kb(lang):
    button_new_feedback = KeyboardButton(text=t(feedback_list_button, lang))
    button_list_feedbacks = KeyboardButton(text=t(feedback_post_button, lang))
    button_back = KeyboardButton(text=t(back_button, lang))

    # Create keyboard markup
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [button_new_feedback, button_list_feedbacks],
            [button_back]
        ],
        resize_keyboard=True
    )
    return keyboard


def score_kb():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="⭐️", callback_data="rate_1"))
    builder.row(InlineKeyboardButton(text="⭐️⭐️", callback_data="rate_2"))
    builder.row(InlineKeyboardButton(text="⭐️⭐️⭐️", callback_data="rate_3"))
    builder.row(InlineKeyboardButton(text="⭐️⭐️⭐️⭐️", callback_data="rate_4"))
    builder.row(InlineKeyboardButton(
        text="⭐️⭐️⭐️⭐️⭐️", callback_data="rate_5"))

    return builder.as_markup()
