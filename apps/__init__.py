from aiogram import Router

from .analyze_app import analyze_routers
from .auth_app import auth_app_routers
from .booking_app import booking_routers
from .clinic_app import doctor_routers
from .feedback_app import feedback_router
from .help import router as help_router
from .scan_qr_app import scan_routers
from .service_app import clinics_routers
from .settings_app import setting_routers
from .start import router as start_router


def handlers_router(dp: Router) -> None:
    dp.include_router(start_router)
    auth_app_routers(dp)
    scan_routers(dp)
    setting_routers(dp)
    feedback_router(dp)
    analyze_routers(dp)
    clinics_routers(dp)
    doctor_routers(dp)
    booking_routers(dp)
    dp.include_router(help_router)
