import os
import tempfile

import psycopg2
import requests
from flask import Flask, jsonify, request

# Настройки Telegram
TELEGRAM_BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"

app = Flask(__name__)


def get_telegram_id_db(phone_number: str):
    # Настройки PostgreSQL
    DB_SETTINGS = {
        "host": os.getenv('DATABASE_HOST'),
        "port": os.getenv('DATABASE_PORT'),
        "database": os.getenv('DATABASE_NAME'),
        "user": os.getenv('DATABASE_USER'),
        "password": os.getenv('DATABASE_PASSWORD')
    }

    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cur = conn.cursor()
        cur.execute(
            "SELECT telegram_id FROM users WHERE phone_number = %s", (
                phone_number,)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return row[0]
        return None
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return None


@app.route('/dock/', methods=['POST'])
def send_pdf():
    data = request.get_json()
    pdf_url = data.get("pdf_url")
    phone_number = data.get("phone_number")
    clicnic_name = data.get("clinic_name")
    date = data.get("date", None)
    date = date.split("T")[0] if date else "unknown_date"
    if len(phone_number) == 9:
        phone_number = "+998" + phone_number
    if not pdf_url or not phone_number:
        return jsonify({"error": "Missing 'pdf_url' or 'phone_number'"}), 400

    try:
        # Скачиваем PDF
        response = requests.get(pdf_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download PDF"}), 400

        # Получаем Telegram ID
        telegram_id = get_telegram_id_db(phone_number)
        if telegram_id is None:
            return jsonify({'error': 'User not found in database'}), 404

        # Сохраняем PDF во временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(response.content)
            tmp_path = tmp_file.name

        # Отправляем в Telegram
        with open(tmp_path, 'rb') as pdf_file:
            send_response = requests.post(
                TELEGRAM_API_URL,
                data={"chat_id": telegram_id},
                files={"document": (
                    f'{clicnic_name}_{date}.pdf', pdf_file, 'application/pdf')}
            )

        os.remove(tmp_path)

        if send_response.status_code != 200:
            return jsonify({"error": "Failed to send PDF to Telegram"}), 500

        return jsonify({"message": "PDF sent successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
