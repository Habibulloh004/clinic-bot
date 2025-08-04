import asyncio
import logging
import os

import redis.asyncio as aioredis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand

from apps import handlers_router
from config import TOKEN

bot = Bot(token="7424582099:AAFBn74y3vZm680TjtuRnm4lcIWPJNDUsyA")
DEBUG = True if os.getenv('DEBUG') == 'True' else False


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/help", description="Получить помощь"),
        BotCommand(command="/restart", description="Перезапустить бота"),
    ]
    await bot.set_my_commands(commands)


async def on_startup():
    """Called when bot starts up"""
    # Clear any existing webhooks to avoid conflicts
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Webhook cleared. Bot is ready for polling.")


async def main() -> None:
    if DEBUG:
        dp = Dispatcher()
    else:
        redis = aioredis.from_url("redis://uzlabs_redis:6379", db=0)  # Use Docker service name
        storage = RedisStorage(redis)
        dp = Dispatcher(storage=storage)

    # Add startup handler
    dp.startup.register(on_startup)
    
    handlers_router(dp)

    await set_commands(bot)
    
    # Add some logging
    logging.info(f"Starting bot polling for bot ID: {(await bot.get_me()).id}")
    
    try:
        await dp.start_polling(bot, skip_updates=True)  # Skip pending updates
    except Exception as e:
        logging.error(f"Error during polling: {e}")
        raise


async def shutdown():
    """Graceful shutdown"""
    logging.info("Shutting down bot...")
    await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен")
        asyncio.run(shutdown())