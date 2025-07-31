from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from apps.analyze_app.logic.text import navigate_next_button, navigate_back_button
from apps.clinic_app.logic.endpoints import get_service_api
from apps.clinic_app.logic.text import back_to_clinic_text
from apps.service_app.logic.endpoints import get_service_by_section_id_api
from utils import t


def clinics_kb(clinics, page: int = 1, lang: str = 'ru'):
    items_per_page = 5
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page

    buttons = []

    clinics_page = clinics[start_idx:end_idx]
    if not clinics_page:
        return None

    for clinic in clinics_page:
        clinic_name = clinic.get("ClinicName", "Без названия")
        clinic_id = clinic.get("Id") if clinic.get("Id") else clinic.get('ClinicId')
        buttons.append([
            InlineKeyboardButton(
                text=clinic_name,
                callback_data=f"clinic_{clinic_id}_{clinic_name}"
            )
        ])

    nav_buttons = []

    if page > 1:
        nav_buttons.append(InlineKeyboardButton(
            text=t(navigate_back_button, lang), callback_data=f"page_{page - 1}"
        ))
    if end_idx < len(clinics):
        nav_buttons.append(InlineKeyboardButton(
            text=t(navigate_next_button, lang), callback_data=f"page_{page + 1}"
        ))

    if nav_buttons:
        buttons.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def services_kb(clinic_id: str, lang: str, page: int = 1, section_id=None) -> InlineKeyboardMarkup:
    """Keyboard for selecting a service in a specific clinic with pagination"""

    ITEMS_PER_PAGE = 5
    if not section_id is None:
        services_data = get_service_by_section_id_api(clinic_id, section_id)
    else:
        services_data = get_service_api(clinic_id)
    if services_data is None:
        return None
    if not services_data:
        return []

    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE

    services_page = services_data[start_idx:end_idx]
    if not services_page:
        return None

    buttons = []

    for service in services_page:
        service_id = service.get("ServiceId")
        service_name = service.get(
            "NameRu") if lang == "ru" else service.get("NameUz")

        if not service_name:
            service_name = "No name"
        buttons.append([
            InlineKeyboardButton(
                text=service_name,
                callback_data=f"service_{clinic_id}_{service_id}"
            )
        ])

    # Navigation buttons (previous/next page)
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(
            text=t(navigate_back_button, lang),
            callback_data=f"page_{page - 1}"
        ))
    if end_idx < len(services_data):
        nav_buttons.append(InlineKeyboardButton(
            text=t(navigate_next_button, lang),
            callback_data=f"page_{page + 1}"
        ))

    if nav_buttons:
        buttons.append(nav_buttons)

    # Button to return to clinic selection
    buttons.append([
        InlineKeyboardButton(text=t(back_to_clinic_text, lang),
                             callback_data="back_to_clinics")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
