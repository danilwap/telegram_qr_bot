import logging, asyncio
import sys

from aiogram.types import Message
from aiogram.filters import CommandStart
from bot import dp, bot

@dp.message(CommandStart)
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())