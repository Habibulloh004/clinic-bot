import asyncio
import logging
import os

import redis.asyncio as aioredis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand

from apps import handlers_router
from config import TOKEN

bot = Bot(token=TOKEN)
DEBUG = True if os.getenv('DEBUG') == 'True' else False


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/help", description="Получить помощь"),
        BotCommand(command="/restart", description="Перезапустить бота"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    if DEBUG:
        dp = Dispatcher()
    else:
        redis = aioredis.from_url("redis://localhost", db=0)
        storage = RedisStorage(redis)
        dp = Dispatcher(storage=storage)

    handlers_router(dp)

    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен")
