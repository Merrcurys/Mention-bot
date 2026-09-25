from pyrogram import Client, filters
from pyrogram.types import Message

from loader import app
from lang import get_text as _
from utils.errors import report_error
from utils.get_admins import get_chat_admins
from utils.get_data import get_chat_data
from utils.sender import is_sender_admin


@app.on_message(filters.command(["access_toggle"]) & filters.group)
async def access_toggle(client: Client, message: Message):
    """Обработчик переключения прав доступа"""
    lang = "en"
    try:
        # Получаем конфигурацию чата
        chat_config = await get_chat_data(message)
        admins = await get_chat_admins(message)
        lang = chat_config.language

        # Проверяем доступ к команде
        if not is_sender_admin(message, admins):
            return await message.reply(_("only_admin", lang))

        # Переключение прав доступа
        chat_config.need_access = not chat_config.need_access
        chat_config.save()

        await message.reply((_("mention_all", lang)
                            if not chat_config.need_access else _("mention_admin", lang)))
    except Exception as e:
        await report_error(
            client, e,
            "Ошибка при переключении прав доступа в чате",
            "Произошла ошибка при переключении прав доступа в чате",
            message=message, lang=lang)
