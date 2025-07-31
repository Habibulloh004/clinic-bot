from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from apps.buttons import *
from utils import t

lang_map = {
    "Русский 🇷🇺": "ru",
    "O'zbek 🇺🇿": "uz"
}


def language_kb() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Русский 🇷🇺"),
             KeyboardButton(text="O'zbek 🇺🇿")],
        ],
        resize_keyboard=True
    )

    return keyboard


def phone_number_kb(lang: str):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=t(phone_number_button, lang),
                    request_contact=True)
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return kb


def menu_kb(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(menu_clinic_button, lang)),
                KeyboardButton(text=t(menu_services_button, lang)),
            ],
            [
                KeyboardButton(text=t(menu_pdf_button, lang)),
                KeyboardButton(text=t(menu_feedback_button, lang)),
            ],
            [
                KeyboardButton(text=t(menu_settings_button, lang)),
                KeyboardButton(text=t(menu_qr_button, lang)),
            ],
            [KeyboardButton(text=t(menu_our_site_button, lang),
                            web_app=WebAppInfo(url="https://uzlabs.uz/"))]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return kb


def gender_kb(lang: str) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(gender_male_button, lang)),
                KeyboardButton(text=t(gender_female_button, lang)),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard
