from loader import logger, ADMIN_CHAT_ID

try:
    from pyrogram.errors import TopicClosed
except ImportError:  # на случай библиотеки без отдельного класса TopicClosed
    TopicClosed = None

TOPIC_CLOSED_ERROR = "TOPIC_CLOSED"


def is_topic_closed(error: Exception) -> bool:
    """Проверяет, что ошибка связана с закрытым топиком.

    Kurigram (форк Pyrogram) определяет отдельное исключение TopicClosed,
    но дополнительно проверяем текст ошибки для совместимости.
    """
    if TopicClosed is not None and isinstance(error, TopicClosed):
        return True

    return TOPIC_CLOSED_ERROR in str(error)


async def report_error(client, error: Exception, log_message: str, admin_message: str):
    """Логирует ошибку и уведомляет о ней администраторский чат.

    Ошибки закрытого топика не отправляются в администраторский чат:
    Telegram сам запрещает отправку сообщений в закрытые топики.
    """
    if is_topic_closed(error):
        logger.warning(f"{log_message} (топик закрыт): {error}")
        return

    logger.error(f"{log_message}: {error}", exc_info=True)
    await client.send_message(ADMIN_CHAT_ID, f"{admin_message}: {error}")
