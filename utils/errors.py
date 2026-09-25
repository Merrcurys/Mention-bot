import asyncio

from loader import logger, ADMIN_CHAT_ID
from lang import get_text as _

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
GENERAL_TOPIC_ID = 1


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


async def _send_to_general(client, chat_id: int, text: str) -> bool:
    """Пытается написать в общий (General) топик форума."""
    for thread_id in (GENERAL_TOPIC_ID, None):
        try:
            await client.send_message(chat_id, text, message_thread_id=thread_id)
            return True
        except Exception as general_error:
            logger.warning(
                f"Не удалось написать в общий топик (thread_id={thread_id}): "
                f"{general_error}")

    return False


async def notify_cannot_send(client, message, error: Exception, lang: str = "en"):
    """Сообщает инициатору, что бот не может писать в топик/чат.

    Порядок: личное сообщение → общий (General) топик → только лог.
    """
    text = _("cannot_send_topic", lang) if is_topic_closed(error) else _("cannot_send_chat", lang)

    # 1. Личное сообщение инициатору
    user = getattr(message, "from_user", None)
    if user is not None:
        try:
            await client.send_message(user.id, text)
            return
        except Exception as dm_error:
            logger.warning(f"Не удалось уведомить в ЛС: {dm_error}")

    # 2. Общий (General) топик — только для топиков/форумов
    chat = getattr(message, "chat", None)
    in_topic = getattr(message, "message_thread_id", None) is not None
    if chat is not None and (in_topic or getattr(chat, "is_forum", False)):
        if await _send_to_general(client, chat.id, text):
            return

    # 3. Ничего не остаётся — уже залогировано выше
    logger.warning("Не удалось уведомить пользователя о невозможности отправки")


async def report_error(
    client,
    error: Exception,
    log_message: str,
    admin_message: str,
    message=None,
    lang: str = "en",
):
    """Логирует ошибку и уведомляет о ней администраторский чат.

    Ожидаемые ошибки (закрытый топик, flood wait, недоступный чат) не
    отправляются в администраторский чат. Если для закрытого топика/чата
    передан message — бот попробует уведомить инициатора (ЛС → General).
    """
    if is_topic_closed(error):
        logger.warning(f"{log_message} (топик закрыт): {error}")
        if message is not None:
            await notify_cannot_send(client, message, error, lang)
        return

    if is_flood_wait(error):
        logger.warning(f"{log_message} (flood wait): {error}")
        return

    if is_chat_unavailable(error):
        logger.warning(f"{log_message} (бот не может писать в чат): {error}")
        if message is not None:
            await notify_cannot_send(client, message, error, lang)
        return

    logger.error(f"{log_message}: {error}", exc_info=True)
    await client.send_message(ADMIN_CHAT_ID, f"{admin_message}: {error}")
