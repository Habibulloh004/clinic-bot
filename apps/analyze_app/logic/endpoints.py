import requests

from config import UZLABS_SERVICES_URL
from db.query import get_phone_number_db
from utils import get_headers


async def get_pdf_by_phone_api(telegram_id: int):
    phone_number = await get_phone_number_db(telegram_id)
    if not phone_number:
        return None
    url = UZLABS_SERVICES_URL + f"genPDF/getByPhone/{phone_number}/"
    headers = get_headers()
    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        return []

    if response.status_code != 200:
        return None

    return response.json()
