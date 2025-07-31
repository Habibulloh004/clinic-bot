from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from apps.buttons import *
from apps.settings_app.logic.text import settings_change_name_button, settings_update_age_button, settings_language_button, \
    settings_notifications_button
from utils import t


def back_kb(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(back_button, lang)),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return kb


def settings_kb(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(settings_change_name_button, lang)),
                KeyboardButton(text=t(settings_update_age_button, lang)),
            ],
            [
                # KeyboardButton(text=_(settings_change_phone_text, lang)),
                KeyboardButton(text=t(settings_language_button, lang)),
                KeyboardButton(text=t(settings_notifications_button, lang)),

            ],
            [
                KeyboardButton(text=t(back_button, lang)),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return kb
