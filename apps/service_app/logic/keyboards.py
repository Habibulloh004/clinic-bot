from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from apps.analyze_app.logic.text import navigate_back_button, navigate_next_button
from apps.buttons import back_button
from apps.clinic_app.logic.text import back_to_clinic_text
from apps.service_app.logic.endpoints import get_service_by_section_api
from apps.service_app.logic.texts import send_location_button
from utils import t


def sections_kb(services, page: int = 0, per_page: int = 5, lang: str = 'ru'):
    # Array of button rows
    inline_keyboard = []

    # Calculate the current services
    start = page * per_page
    end = start + per_page
    current_services = services[start:end]

    # Add buttons for services
    for service in current_services:
        name = service["NameUz"] if lang == 'uz' else service["NameRu"]
        button = InlineKeyboardButton(
            text=name,
            callback_data=f"section_{service['Id']}_{name}"
        )
        # Each button in a separate row. Can be grouped by 2 if needed.
        inline_keyboard.append([button])

    # "Back" and "Next" buttons
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(
            text=t(navigate_back_button, lang), callback_data=f"page_{page - 1}"
        ))
    if end < len(services):
        navigation_buttons.append(InlineKeyboardButton(
            text=t(navigate_next_button, lang), callback_data=f"page_{page + 1}"
        ))

    if navigation_buttons:
        inline_keyboard.append(navigation_buttons)

    # Create the markup
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard




def clinics_keyboard(clinics, page: int = 0, per_page: int = 5, lang: str = 'ru'):
    # Array of button rows
    inline_keyboard = []

    # Calculate the current clinics
    start = page * per_page
    end = start + per_page
    current_clinics = clinics[start:end]

    # Add buttons for clinics
    for clinic in current_clinics:
        button = InlineKeyboardButton(
            text=clinic["ClinicName"],
            callback_data=f"clinic_{clinic['ClinicId']}_{clinic["ClinicName"]}"
            # callback_data=f"clinic_{clinic['ClinicId']}"
        )
        # Each button in a separate row. Can be grouped in pairs if needed.
        inline_keyboard.append([button])

    # "Back" and "Next" buttons
    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(
            text=t(navigate_back_button, lang), callback_data=f"page_{page - 1}"
        ))
    if end < len(clinics):
        navigation_buttons.append(InlineKeyboardButton(
            text=t(navigate_next_button, lang), callback_data=f"page_{page + 1}"
        ))

    if navigation_buttons:
        inline_keyboard.append(navigation_buttons)

    # Create the markup
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard


def location_kb(lang: str = 'ru'):
    keyboards = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(send_location_button,
                                   lang), request_location=True)],
            [KeyboardButton(text=t(back_button, lang))]
        ],
        resize_keyboard=True
    )
    return keyboards


def services_by_section_id_kb(clinic_id: str, section_id: str, lang: str, page: int = 1):
    """Keyboard for selecting a service in a specific clinic with pagination"""

    ITEMS_PER_PAGE = 5

    services_data = get_service_by_section_api(clinic_id, section_id)
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
                             callback_data="back_to_clinics"
                             )
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
