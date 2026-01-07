"""
edit_media_prevent_duplicate

Вспомогательный инструмент для Telegram-бота на aiogram.

Назначение:
- безопасно вызывать edit_media() для сообщений;
- предотвращать падение бота при повторных / быстрых кликах пользователя
  (TelegramBadRequest: message is not modified);
- вместо ошибки показывать пользователю понятный alert
  с просьбой подождать.

Использование:
Функция вызывается из callback-хендлеров.
Возвращает True при успешном обновлении сообщения
или False, если действие было проигнорировано (duplicate).

Модуль не реализует антиспам или rate limit —
он мягко обрабатывает повторные вызовы Telegram API
и улучшает пользовательский опыт.
"""

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InputMediaPhoto



async def edit_media_prevent_duplicate(
    call: CallbackQuery,
    media: InputMediaPhoto,
    reply_markup=None,
    alert_text: str = "Пожалуйста, подождите 🙂\nИзображение обновляется."
) -> bool:
    """
    Безопасно редактирует media в сообщении.
    Предотвращает ошибку Telegram при повторных / быстрых кликах
    и показывает пользователю alert вместо падения бота.

    :return: True — если edit_media выполнен
             False — если произошёл duplicate / not modified
    """
    try:
        await call.message.edit_media(
            media=media,
            reply_markup=reply_markup
        )
        await call.answer()
        return True

    except TelegramBadRequest:
        # Чаще всего: message is not modified (двойной клик)
        await call.answer(alert_text, show_alert=True)
        return False
