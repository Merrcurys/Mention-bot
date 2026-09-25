import asyncio

from models.models import ChatConfig


def _get_or_create(chat_id: int) -> ChatConfig:
    """Синхронно достаёт или создаёт конфигурацию чата."""
    chat_config, _ = ChatConfig.get_or_create(chat_id=chat_id)
    return chat_config


async def get_chat_data(message) -> ChatConfig:
    """Возвращает конфигурацию чата, создавая её при необходимости.

    Всегда возвращает объект конфигурации; при ошибке БД исключение
    пробрасывается, чтобы вызывающий код залогировал реальную причину,
    а не падал потом на ``chat_config.language``.
    """
    return await asyncio.to_thread(_get_or_create, message.chat.id)
