from pyrogram import enums

from loader import app


async def get_chat_admins(message) -> list[int]:
    """Возвращает список идентификаторов администраторов чата.

    При ошибке получения исключение пробрасывается: иначе сбой API был бы
    принят за «пользователь не администратор» и админ получил бы отказ.
    """
    admins = []

    async for member in app.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        admins.append(member.user.id)

    return admins
