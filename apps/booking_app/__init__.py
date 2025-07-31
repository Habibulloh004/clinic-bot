from aiogram import Dispatcher

from .doctor import router as doctor_router
from .day import router as day_router
from .time import router as time_router
from .comment import router as comment_router

from aiogram import Router
def booking_routers(dp: Router):
    dp.include_router(doctor_router)
    dp.include_router(day_router)
    dp.include_router(time_router)
    dp.include_router(comment_router)
