import asyncio

from loader import logger, ADMIN_CHAT_ID

try:
    from pyrogram.errors import TopicClosed
except ImportError:  # на случай библиотеки без отдельного класса TopicClosed
    TopicClosed = None

try:
    from pyrogram.errors import FloodWait
except ImportError:
    FloodWait = None

TOPIC_CLOSED_ERROR = "TOPIC_CLOSED"
FLOOD_WAIT_ERROR = "FLOOD_WAIT"
CHAT_UNAVAILABLE_ERRORS = (
    "CHANNEL_PRIVATE",
    "CHAT_WRITE_FORBIDDEN",
    "USER_BANNED_IN_CHANNEL",
    "CHAT_ADMIN_REQUIRED",
)


def is_topic_closed(error: Exception) -> bool:
    """Проверяет, что ошибка связана с закрытым топиком.

    Kurigram (форк Pyrogram) определяет отдельное исключение TopicClosed,
    но дополнительно проверяем текст ошибки для совместимости.
    """
    if TopicClosed is not None and isinstance(error, TopicClosed):
        return True

    return TOPIC_CLOSED_ERROR in str(error)


def is_flood_wait(error: Exception) -> bool:
    """Проверяет, что Telegram просит подождать (FLOOD_WAIT)."""
    if FloodWait is not None and isinstance(error, FloodWait):
        return True

    return FLOOD_WAIT_ERROR in str(error)


def is_chat_unavailable(error: Exception) -> bool:
    """Ошибки, при которых бот в принципе не может писать в чат.

    CHANNEL_PRIVATE (бот кикнут/нет доступа), CHAT_WRITE_FORBIDDEN (нет прав),
    USER_BANNED_IN_CHANNEL (забанен), CHAT_ADMIN_REQUIRED. Это не ошибки кода,
    поэтому в администраторский чат они не отправляются.
    """
    text = str(error)
    return any(marker in text for marker in CHAT_UNAVAILABLE_ERRORS)


async def call_with_flood_wait(coro_factory, max_retries: int = 3):
    """Выполняет корутину, пережидая FLOOD_WAIT и повторяя запрос.

    coro_factory — функция без аргументов, возвращающая новую корутину:
    await call_with_flood_wait(lambda: message.reply(text)).
    """
    for attempt in range(max_retries + 1):
        try:
            return await coro_factory()
        except Exception as error:
            if not is_flood_wait(error) or attempt == max_retries:
                raise

            try:
                wait = int(getattr(error, "value", 0) or 0)
            except (TypeError, ValueError):
                wait = 0

            logger.warning(
                f"FLOOD_WAIT: ждём {wait} c и повторяем отправку "
                f"(попытка {attempt + 1}/{max_retries})")
            await asyncio.sleep(wait + 1)


async def report_error(client, error: Exception, log_message: str, admin_message: str):
    """Логирует ошибку и уведомляет о ней администраторский чат.

    Ожидаемые ошибки (закрытый топик, flood wait, недоступный чат) не
    отправляются в администраторский чат, чтобы не спамить.
    """
    if is_topic_closed(error):
        logger.warning(f"{log_message} (топик закрыт): {error}")
        return

    if is_flood_wait(error):
        logger.warning(f"{log_message} (flood wait): {error}")
        return

    if is_chat_unavailable(error):
        logger.warning(f"{log_message} (бот не может писать в чат): {error}")
        return

    logger.error(f"{log_message}: {error}", exc_info=True)
    await client.send_message(ADMIN_CHAT_ID, f"{admin_message}: {error}")
