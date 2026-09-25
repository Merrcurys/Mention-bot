from pyrogram import Client, filters
from pyrogram.types import Message

from loader import app
from lang import get_text as _
from utils.errors import report_error
from utils.get_admins import get_chat_admins
from utils.get_data import get_chat_data
from utils.sender import is_sender_admin


@app.on_message(filters.command(["names_visibility"]) & filters.group)
async def names_visibility_toggle(client: Client, message: Message):
    """Обработчик переключения видимости никнеймов"""
    try:
        # Получаем конфигурацию чата
        chat_config = await get_chat_data(message)
        admins = await get_chat_admins(message)
        lang = chat_config.language

        # Проверяем доступ к команде
        if not is_sender_admin(message, admins):
            return await message.reply(_("only_admin", lang))

        # Переключение видимости никнеймов
        chat_config.is_nickname_visible = not chat_config.is_nickname_visible
        chat_config.save()

        await message.reply(_("show_username", lang)
                            if chat_config.is_nickname_visible else _("hide_username", lang))
    except Exception as e:
        await report_error(
            client, e,
            "Ошибка при переключении видимости имен в чате",
            "Произошла ошибка при переключении видимости имен в чате")
