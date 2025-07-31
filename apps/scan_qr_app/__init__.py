from aiogram import Router

from .start import router as start_router


def scan_routers(dp: Router):
    dp.include_router(start_router)
