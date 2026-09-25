from pyrogram import Client, filters
from pyrogram.types import Message

from loader import app, logger, ADMIN_CHAT_ID
from keyboard.keyboard_buttons import keyboard_start_ru, keyboard_start_gb
from lang import get_lang_by_code, get_text as _


@app.on_message(filters.private)
async def start_command(client: Client, message: Message):
    """Выводит инфо сообщение с кнопкой для добавления бота в группу."""
    try:
        # Язык определяем по клиенту Telegram, иначе английский
        lang = get_lang_by_code(getattr(message.from_user, "language_code", None))
        keyboard = keyboard_start_ru if lang == "ru" else keyboard_start_gb

        await message.reply_text(_("start_text", lang), reply_markup=keyboard)
    except Exception as e:
        logger.error(
            f"Ошибка при отправке стартового сообщения пользователю: {e}", exc_info=True)
        await client.send_message(
            ADMIN_CHAT_ID,
            f"Произошла ошибка при отправке стартового сообщения пользователю: {e}")
