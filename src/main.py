import asyncio

from telegramQRbot.utils.db.core import DatabaseManager
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "my_database.db"
from logging_config import get_logger
from telegramQRbot.bot import bot, dp
from telegramQRbot import setup_routers
from telegramQRbot.config import Config
from infrastructure.redis_client import get_redis

logger = get_logger(__name__)
from pathlib import Path
from dotenv import load_dotenv
import os

from telegramQRbot.middlewares.config import ConfigMiddleware



BASE_DIR = Path(__file__).resolve().parent.parent  # src → project

# Загружаем общий .env
load_dotenv(BASE_DIR / ".env")


BOT_TOKEN = os.getenv("BOT_TOKEN")
DEV_CHECK = os.getenv("DEV_CHECK")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMINS = os.getenv("ADMINS", "")
ADMINS = ADMINS.split(",") if ADMINS else []


async def main() -> None:
    redis = get_redis()
    await redis.ping()

    db = DatabaseManager(DB_PATH)
    db.create_tables()  # если create_tables сделаешь async, или просто вызов db.create_tables()

    # Подготавливаем данные для конфига
    cfg = Config(
        dev_check=DEV_CHECK,
        channel_id=CHANNEL_ID,
        admins=ADMINS
    )

    dp['db'] = db
    dp.update.middleware(ConfigMiddleware(cfg))


    try:
        logger.info('Bot started.')
        setup_routers(dp)
        await dp.start_polling(bot)

    finally:
        # При завершении работы закрываем базу
        redis = get_redis()
        await redis.close()

        db.close()
        logger.info('Bot stopped and database connection closed.')


if __name__ == '__main__':
    asyncio.run(main())