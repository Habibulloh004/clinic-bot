import requests

from config import UZLABS_SERVICES_URL
from utils import get_headers


def get_clinics_api():
    url = UZLABS_SERVICES_URL + "clinics/all"
    headers = get_headers()

    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        return []
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_service_api(clinic_id: str):
    url = UZLABS_SERVICES_URL + f"clinics/services/{clinic_id}"
    headers = get_headers()

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    services_data = response.json()
    return services_data


def get_clinic_services_by_name_api(clinic_name: str):
    url = UZLABS_SERVICES_URL + f"clinics/search/{clinic_name}"
    headers = get_headers()

    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        return []

    services_data = response.json()
    return services_data


def get_reservation_timetable_api(clinic_id: int, service_id: int, lang):
    url = UZLABS_SERVICES_URL + \
        f"reservation/getTimetable/{clinic_id}/{service_id}"
    headers = get_headers()

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None, None

    reservation_data = response.json()
    result = {}
    for i, key in enumerate(reservation_data.keys(), start=1):
        result[key] = f"Врач {i}" if lang == 'ru' else f'Shifokor {i}'
    return result, reservation_data


def add_reservation_api(
        user_name: str,
        birthday: str,
        gender: int,
        phone: str,
        come_date: str,
        clinic_id: int,
        doctor_id: str,
        service_id: int,
        comment: str
):
    url = UZLABS_SERVICES_URL + "reservation/add"
    headers = get_headers()
    payload = {
        "user_name": user_name,
        "dayofbith": birthday,
        "gender": gender,
        "user_phone": phone,
        "come_data": come_date,
        "clinic_id": clinic_id,
        "doctor_id": doctor_id,
        "service_id": service_id,
        "comment": comment
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 404:
        data = response.json()
        if data.get('error') == 'You have used all your limits.':
            return response.status_code
        else:
            return 401
    return response.status_code


def get_notification_templates_api():
    url = UZLABS_SERVICES_URL + "notifiClinics/templates"
    headers = get_headers()

    response = requests.get(url, headers=headers)
    return response.json()


def create_notification_api(
        clinic_id: int,
        service_id: int,
        doctor_id: str,
        message_uz: str,
        message_ru: str
):
    url = UZLABS_SERVICES_URL + "notifiClinics/create"
    payload = {
        "clinic_id": clinic_id,
        "service_id": service_id,
        "doctor_id": doctor_id,
        "message_uz": message_uz,
        "message_ru": message_ru,
    }
    headers = get_headers()
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
