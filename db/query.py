import asyncpg

from config import DATABASE_PORT, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_HOST


async def db_connection():
    return await asyncpg.create_pool(
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME,
        host=DATABASE_HOST,
        port=DATABASE_PORT
    )


async def save_user_db(telegram_id: int,
                       phone_number: str,
                       language: str,
                       name: str = '',
                       gender: int = 0,
                       birthday: str = ''):
    db_pool = await db_connection()

    async with db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (telegram_id, phone_number, language, name, gender, birthday)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (telegram_id) DO UPDATE
            SET phone_number = EXCLUDED.phone_number,
                language = EXCLUDED.language,
                name = EXCLUDED.name,
                gender = EXCLUDED.gender,
                birthday = EXCLUDED.birthday
        """, telegram_id, phone_number, language, name, gender, birthday)


async def get_phone_number_db(telegram_id: int):
    db_pool = await db_connection()

    async with db_pool.acquire() as conn:
        result = await conn.fetchrow("""
            SELECT phone_number 
            FROM users 
            WHERE telegram_id = $1
        """, telegram_id)

    if result:
        return result['phone_number']
    return None


async def get_datas_db(telegram_id: int):
    db_pool = await db_connection()

    async with db_pool.acquire() as conn:
        result = await conn.fetchrow("""
            SELECT *
            FROM users 
            WHERE telegram_id = $1
        """, telegram_id)

    if result:
        return result
    return None
