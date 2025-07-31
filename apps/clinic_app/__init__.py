from aiogram import Router

from .clinic import router as clinic_router
from .search import router as search_router
from .service import router as service_router
from .start import router as start_router


def doctor_routers(dp: Router):
    dp.include_router(start_router)
    dp.include_router(clinic_router)
    dp.include_router(service_router)
    dp.include_router(search_router)
