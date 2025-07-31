import requests

from config import UZLABS_SERVICES_URL
from utils import get_headers


def add_remark_api(service_id: int, score: int, comment: str = ""):
    url = UZLABS_SERVICES_URL + "remark/add"
    print(service_id)
    headers = get_headers()
    payload = {
        "service_id": service_id,
        "score": score,
        "comment": comment
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def list_remark_by_clinic_id_api(clinic_id):
    url = UZLABS_SERVICES_URL + f"remark/list/{clinic_id}"
    headers = get_headers()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None
