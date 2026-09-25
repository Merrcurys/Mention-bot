from pyrogram import Client, filters
from pyrogram.types import Message

from loader import app
from keyboard.keyboard_buttons import keyboard_help
from lang import get_text as _
from utils.errors import report_error
from utils.get_data import get_chat_data


@app.on_message(filters.command(["help", "command"]) & filters.group)
async def help_command(client: Client, message: Message):
    """Выводит справку по всем командам."""
    try:
        chat_config = await get_chat_data(message)

        # Получаем статус по командам
        help_3_command = "help_text_3_only" if chat_config.need_access else "help_text_3_many"
        help_4_command = "help_text_4_show" if chat_config.is_nickname_visible else "help_text_4_hide"

        # Формируем текст
        text = _("help_text_start", chat_config.language) + \
            _(help_3_command, chat_config.language) + \
            _(help_4_command, chat_config.language) + \
            _("help_text_end", chat_config.language)

        await message.reply_text(text, reply_markup=keyboard_help, disable_web_page_preview=True,)
    except Exception as e:
        await report_error(
            client, e,
            "Ошибка при отправке сообщения справки в чат",
            "Произошла ошибка при отправке справки в чат")
