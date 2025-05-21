from pyrogram import enums
from loader import app, logger


async def get_chat_admins(message):
    """Возвращает список идентификаторов администраторов чата."""
    admins = []
    try:
        async for member in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            admins.append(member.user.id)
    except Exception as e:
        logger.error(
            f"Ошибка при получении администраторов чата: {e}", exc_info=True)
    return admins
