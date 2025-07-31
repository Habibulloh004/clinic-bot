import requests

url = 'http://127.0.0.1:5000/send-pdf/'

response = requests.post(url, json={
    'pdf_url': "https://bugs.python.org/file47781/Tutorial_EDIT.pdf",
    'phone_number': '+998970200055',
    'clinic_name': "Test Clinic",
    'date': "2023-10-01T12:00:00",
})

if response.status_code:
    print(response.json())
