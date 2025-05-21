from pyrogram import Client, filters
from pyrogram.types import Message

from loader import app, logger, ADMIN_CHAT_ID
from keyboard.keyboard_buttons import keyboard_help
from lang import get_text as _
from utils.get_data import get_chat_data


@app.on_message(filters.command(["help", "command"]) & filters.group)
async def help_command(client: Client, message: Message):
    """Выводит справку по всем командам."""
    try:
        chat_config = await get_chat_data(message)
        await message.reply_text(_("help_text", chat_config.language),
                                 reply_markup=keyboard_help, disable_web_page_preview=True,)
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения справки в чат: {e}", exc_info=True)
        await client.send_message(ADMIN_CHAT_ID, f"Произошла ошибка при отправке справки в чат: {e}")