from pyrogram import Client, filters
from pyrogram.types import Message

from loader import app, logger, ADMIN_CHAT_ID
from keyboard.keyboard_buttons import keyboard_start_gb
from lang import get_text as _
from utils.monitoring import track_command


@app.on_message(filters.private)
@track_command("start")
async def start_command(client: Client, message: Message):
    """Выводит инфо сообщение с кнопкой для добавления бота в группу."""
    try:
        await message.reply_text(_('start_text'),
                                 reply_markup=keyboard_start_gb, disable_web_page_preview=True,)
    except Exception as e:
        logger.error(
            f"Ошибка при отправке стартового сообщения пользователю: {e}", exc_info=True)
        await client.send_message(ADMIN_CHAT_ID, f"Произошла ошибка при отправке стартового сообщения пользователю.")
