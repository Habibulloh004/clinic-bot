from aiogram import Router

from .start import router as start_router


def auth_app_routers(dp: Router):
    dp.include_router(start_router)
