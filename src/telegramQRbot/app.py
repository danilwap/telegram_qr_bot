from aiogram import Dispatcher
from telegramQRbot.handlers.user import router as qr_router

def setup_routers(dp: Dispatcher) -> None:
    dp.include_router(qr_router)