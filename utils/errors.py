from loader import logger, ADMIN_CHAT_ID

TOPIC_CLOSED_ERROR = "TOPIC_CLOSED"


def is_topic_closed(error: Exception) -> bool:
    """Проверяет, что ошибка связана с закрытым топиком.

    В Pyrogram 2.0.106 нет отдельного исключения для TOPIC_CLOSED,
    поэтому ошибку определяем по её тексту.
    """
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
