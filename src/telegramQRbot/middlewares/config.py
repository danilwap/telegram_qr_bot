from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from telegramQRbot.config import Config

class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config: Config):
        self.config = config

    async def __call__(self, handler, event: TelegramObject, data: dict):
        data["config"] = self.config
        return await handler(event, data)
