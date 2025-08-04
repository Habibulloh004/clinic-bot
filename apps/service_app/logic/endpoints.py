import requests
from config import UZLABS_SERVICES_URL
from utils import get_headers

def get_sections_endpoint():
    try:
        if not UZLABS_SERVICES_URL:
            print("Warning: UZLABS_SERVICES_URL not configured")
            return []
        url = UZLABS_SERVICES_URL + "clinics/sections"
        headers = get_headers()
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return []
        if response.status_code != 200:
            return None
        return response.json()
    except Exception as e:
        print(f"Error fetching sections: {e}")
        return []

def get_service_by_section_id_api(clinic_id: str, section_id: str):
    try:
        if not UZLABS_SERVICES_URL:
            print("Warning: UZLABS_SERVICES_URL not configured")
            return None
        url = UZLABS_SERVICES_URL + f"clinics/services/{clinic_id}/{section_id}"
        headers = get_headers()
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        return response.json()
    except Exception as e:
        print(f"Error fetching services by section: {e}")
        return None

def get_service_by_section_api(clinic_id: str, section_id):
    try:
        if not UZLABS_SERVICES_URL:
            return None
        url = UZLABS_SERVICES_URL + f"clinics/services/{clinic_id}/{section_id}"
        headers = get_headers()
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        return response.json()
    except Exception as e:
        print(f"Error fetching services by section: {e}")
        return None

def post_get_clinics_nearby_endpoint(lat, lon, section_id, lang: str = 'ru'):
    try:
        if not UZLABS_SERVICES_URL:
            return []
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
    except Exception as e:
        print(f"Error fetching nearby clinics: {e}")
        return []