from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent  # src → project

# Загружаем общий .env
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEV_CHECK = os.getenv("DEV_CHECK")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMINS = os.getenv("ADMINS", "")
ADMINS = ADMINS.split(",") if ADMINS else []


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)
storage = MemoryStorage()
dp = Dispatcher()
