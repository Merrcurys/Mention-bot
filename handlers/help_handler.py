from pyrogram import Client, filters
from pyrogram.types import Message

from loader import app
from keyboard.keyboard_buttons import keyboard_help
from lang import get_help_text
from utils.errors import report_error
from utils.get_data import get_chat_data


@app.on_message(filters.command(["help", "command"]) & filters.group)
async def help_command(client: Client, message: Message):
    """Выводит справку по всем командам."""
    lang = "en"
    try:
        chat_config = await get_chat_data(message)
        lang = chat_config.language

        await message.reply_text(get_help_text(chat_config), reply_markup=keyboard_help)
    except Exception as e:
        await report_error(
            client, e,
            "Ошибка при отправке сообщения справки в чат",
            "Произошла ошибка при отправке справки в чат",
            message=message, lang=lang)
