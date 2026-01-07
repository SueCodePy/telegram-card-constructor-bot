"""
Точка входа Telegram-бота для создания поздравительных открыток.

Настраивает логирование, регистрирует роутеры
и запускает бота в режиме polling.
"""
import asyncio
from bot.bot import dp, bot
from bot.handlers import router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

async def main():
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())