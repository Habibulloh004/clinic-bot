import requests

from config import UZLABS_SERVICES_URL
from utils import get_headers


def get_sections_endpoint():
    url = UZLABS_SERVICES_URL + "clinics/sections"
    headers = get_headers()
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        return []
    if response.status_code != 200:
        return None
    return response.json()


def get_service_by_section_id_api(clinic_id: str, section_id: str):
    url = UZLABS_SERVICES_URL + f"clinics/services/{clinic_id}/{section_id}"
    headers = get_headers()

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    services_data = response.json()
    return services_data


def get_service_by_section_api(clinic_id: str, section_id):
    url = UZLABS_SERVICES_URL + f"clinics/services/{clinic_id}/{section_id}"
    headers = get_headers()

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    services_data = response.json()
    return services_data


def post_get_clinics_nearby_endpoint(lat, lon, section_id, lang: str = 'ru'):
    url = UZLABS_SERVICES_URL + "clinics/sections/getclinics"
    headers = get_headers()
    payload = {
        "longitude": str(lon),
        "latitude": str(lat),
        "sectionID": int(section_id)
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 404:
        return []
    if response.status_code != 200:
        return None
    return response.json()


data = get_sections_endpoint()
import json

from apps.service_app.logic.endpoints import data

if __name__ == "__main__":
    # Example usage
    print(json.dumps(data, indent=4))
