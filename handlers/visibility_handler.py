import asyncio

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
    lang = "en"
    try:
        # Получаем конфигурацию чата
        chat_config = await get_chat_data(message)
        admins = await get_chat_admins(message)
        lang = chat_config.language

        # Проверяем доступ к команде
        if not is_sender_admin(message, admins):
            return await message.reply(_("only_admin", lang))

        # Сначала подтверждаем в чате, и только потом сохраняем настройку
        new_visibility = not chat_config.is_nickname_visible
        await message.reply(
            _("show_username", lang)
            if new_visibility else _("hide_username", lang))

        chat_config.is_nickname_visible = new_visibility
        await asyncio.to_thread(chat_config.save)
    except Exception as e:
        await report_error(
            client, e,
            "Ошибка при переключении видимости имен в чате",
            "Произошла ошибка при переключении видимости имен в чате",
            message=message, lang=lang)
