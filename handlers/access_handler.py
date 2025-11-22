from pyrogram import Client, filters
from pyrogram.types import Message

from loader import app, logger, ADMIN_CHAT_ID
from lang import get_text as _
from utils.get_admins import get_chat_admins
from utils.get_data import get_chat_data
from utils.monitoring import track_command


@app.on_message(filters.command(["access_toggle"]) & filters.group)
@track_command("access_toggle")
async def access_toggle(client: Client, message: Message):
    """Обработчик переключения прав доступа"""
    try:
        # Получаем конфигурацию чата
        chat_config = await get_chat_data(message)
        admins = await get_chat_admins(message)
        lang = chat_config.language

        # Проверяем доступ к команде
        if message.from_user.id not in admins:
            return await message.reply(_("only_admin", lang))

        # Переключение прав доступа
        chat_config.need_access = not chat_config.need_access
        chat_config.save()

        await message.reply((_("mention_all", lang)
                            if not chat_config.need_access else _("mention_admin", lang)))
    except Exception as e:
        logger.error(
            f"Ошибка при переключении прав доступа в чате: {e}", exc_info=True)
        await client.send_message(ADMIN_CHAT_ID, f"Произошла ошибка при переключении прав доступа в чате: {e}")
