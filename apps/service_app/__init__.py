from aiogram import Router

from .clinics import router as clinics_router
from .location import router as location_router
from .section import router as section_router
from .start import router as start_router


def clinics_routers(dp: Router):
    dp.include_router(location_router)
    dp.include_router(clinics_router)
    dp.include_router(start_router)
    dp.include_router(section_router)
