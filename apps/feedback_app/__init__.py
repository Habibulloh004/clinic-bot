from aiogram import Router

from .create import router as create_router
from .list import router as list_router
from .start import router as start_router


def feedback_router(dp: Router):
    dp.include_router(create_router)
    dp.include_router(list_router)
    dp.include_router(start_router)
