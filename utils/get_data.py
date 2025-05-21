from loader import logger
from models.models import ChatConfig
from models.utils import create_table_if_not_exists


async def get_chat_data(message):
    """Возвращает конфигурацию чата."""
    try:
        create_table_if_not_exists(chat_id=message.chat.id)
        chat_config = ChatConfig.get(ChatConfig.chat_id == message.chat.id)
        return chat_config
    except Exception as e:
        logger.error(
            f"Ошибка при получении конфигурации чата: {e}", exc_info=True)
        return None
