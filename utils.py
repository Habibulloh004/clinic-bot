from datetime import datetime

from config import UZLABS_TOKEN
from middleware import LanguageMiddleware


def t(texts: dict, lang: str) -> str:
    return texts.get(lang, texts['uz'])


def get_language(telegram_id) -> str:
    lang = LanguageMiddleware.get_language(telegram_id)
    return lang


def datetime_converter(date_str):
    dt = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
    folder_name = dt.strftime("%Y-%m-%d_%H-%M-%S")
    return folder_name


def get_headers():
    headers = {
        "Authorization": f"Bearer {UZLABS_TOKEN}",
        "Content-Type": "application/json"
    }
    return headers
