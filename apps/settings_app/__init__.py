from aiogram import Router

from .age import router as age_router
from .back import router as back_router
from .language import router as language_router
from .name import router as name_router
from .notification import router as notification_router
from .phone import router as phone_router
from .start import router as start_router


def setting_routers(dp: Router):
    dp.include_router(age_router)
    dp.include_router(notification_router)
    dp.include_router(language_router)
    dp.include_router(name_router)
    dp.include_router(phone_router)
    dp.include_router(back_router)
    dp.include_router(start_router)
