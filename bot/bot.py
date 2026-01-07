"""
Инициализация Telegram-бота и диспетчера.

Создаёт экземпляры Bot и Dispatcher
с базовыми настройками проекта.
"""

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties

from config import settings

dp = Dispatcher()
bot = Bot(settings.BOT, default=DefaultBotProperties(parse_mode='HTML'))