import psycopg2

from config import (DATABASE_HOST, DATABASE_NAME, DATABASE_PASSWORD,
                    DATABASE_PORT, DATABASE_USER)


class LanguageMiddleware:
    conn = psycopg2.connect(
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT
    )

    @classmethod
    def get_language(cls, telegram_id):
        with cls.conn.cursor() as cur:
            cur.execute(
                "SELECT language FROM users WHERE telegram_id = %s", (
                    telegram_id,)
            )
            result = cur.fetchone()
            return result[0] if result else "ru"

    @classmethod
    def set_language(cls, telegram_id, lang):
        with cls.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (telegram_id, language)
                VALUES (%s, %s)
                ON CONFLICT (telegram_id) DO UPDATE SET language = EXCLUDED.language
            """, (telegram_id, lang))
            cls.conn.commit()
