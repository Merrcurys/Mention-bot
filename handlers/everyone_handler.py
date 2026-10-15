import asyncio
import math
import time
from html import escape

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from loader import app
from lang import get_text as _
from utils.errors import call_with_flood_wait, report_error
from utils.get_admins import get_chat_admins
from utils.get_data import get_chat_data
from utils.sender import get_sender_id, is_sender_admin


MAX_USERS = 75
BATCH_SIZE = 5
MIN_SEND_DELAY = 1
# chat_id -> время (monotonic), до которого команда недоступна
frozen_commands = {}
FROZEN_SECONDS = 60


def _is_frozen(chat_id: int) -> bool:
    until = frozen_commands.get(chat_id)
    return until is not None and time.monotonic() < until


def _seconds_left(chat_id: int) -> int:
    """Сколько секунд осталось до снятия заморозки команды."""
    until = frozen_commands.get(chat_id)
    if until is None:
        return 0
    return max(0, math.ceil(until - time.monotonic()))


def _freeze(chat_id: int) -> None:
    now = time.monotonic()
    for expired in [cid for cid, until in frozen_commands.items() if until <= now]:
        frozen_commands.pop(expired, None)
    frozen_commands[chat_id] = now + FROZEN_SECONDS


@app.on_message(filters.command(["all", "here", "everyone"]) & filters.group)
async def everyone_command(client: Client, message: Message):
    """Обработчик команды для оповещения всех пользователей."""
    lang = "en"
    try:
        # Получаем конфигурацию чата
        chat_config = await get_chat_data(message)
        lang = chat_config.language

        # Проверяем доступ к команде (админов запрашиваем только при необходимости)
        if chat_config.need_access:
            admins = await get_chat_admins(message)
            if not is_sender_admin(message, admins):
                return await message.reply(_("only_admin", lang))

        # Проверяем заморожена ли команда
        if _is_frozen(message.chat.id):
            text = _("spam_control", lang).format(seconds=_seconds_left(message.chat.id))
            return await message.reply(text)

        # Собираем участников (без ботов, удалённых и отправителя)
        users = await collect_users(message)
        if users is None:
            return await message.reply(_("many_users", lang))
        if not users:
            return await message.reply(_("no_users_found", lang))

        # Замораживаем сразу, до отправки, чтобы параллельные /all не дублировались
        _freeze(message.chat.id)
        await send_user_links(message, users, chat_config, lang)
    except Exception as e:
        await report_error(
            app, e,
            "Ошибка при выполнении команды /all в чате",
            "Произошла ошибка при выполнении /all в чате",
            message=message, lang=lang)


async def collect_users(message: Message):
    """Возвращает список участников для оповещения.

    Пропускает ботов, удалённых пользователей и самого отправителя.
    Если подходящих больше MAX_USERS — возвращает None, не вычитывая
    список участников целиком.
    """
    sender_id = get_sender_id(message)
    users = []

    async for member in app.get_chat_members(message.chat.id):
        user = member.user
        if user.is_bot or user.is_deleted or sender_id == user.id:
            continue

        users.append(user)
        if len(users) > MAX_USERS:
            return None

    return users


async def get_slowmode_delay(chat_id: int) -> int:
    """Медленный режим чата в секундах (0, если выключен).

    Telegram не отдаёт slowmode в апдейте, поэтому запрашиваем чат.
    """
    try:
        chat = await app.get_chat(chat_id)
    except Exception:
        return 0
    return int(getattr(chat, "slow_mode_delay", 0) or 0)


async def is_bot_admin(chat_id: int) -> bool:
    """Является ли сам бот администратором чата."""
    try:
        member = await app.get_chat_member(chat_id, app.me.id)
    except Exception:
        return False
    return member.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    )


def _format_batch(prefix: str, links: str, lang: str, visible: bool) -> str:
    """Собирает текст сообщения с оповещениями.

    Видимые имена идут с новой строки под заголовком, а скрытые ссылки
    (из невидимых символов) — на первой строке, без отступа.
    """
    header = f"{prefix}{_('all_info', lang)}"
    return f"{header}\n{links}" if visible else f"{header}{links}"


async def send_user_links(message: Message, users, chat_config, lang):
    """Отправляет сообщения со ссылками на пользователей в чате."""
    try:
        # В чате с медленным режимом шлём не чаще, чем разрешено, чтобы
        # не ловить SLOWMODE_WAIT и не ждать лишний раз в ретраях.
        slowmode = await get_slowmode_delay(message.chat.id)
        delay = max(MIN_SEND_DELAY, slowmode)

        # Если чат в медленном режиме, а бот не админ — ограничение
        # действует и на него. Предупреждаем об этом в первом сообщении.
        prefix = ""
        if slowmode and not await is_bot_admin(message.chat.id):
            prefix = _("slowmode_admin_hint", lang)

        link_users = []

        for user in users:
            # Формируем ссылку на пользователя
            if chat_config.is_nickname_visible:
                # Имя экранируем, чтобы символы [ ] ( ) _ * не ломали разметку
                name = escape(user.username or user.first_name or str(user.id))
                link_users.append(f'<a href="tg://user?id={user.id}">@{name}</a>, ')
            else:
                # Используем невидимый символ (U+200b) для скрытия имени пользователя
                link_users.append(f'<a href="tg://user?id={user.id}">\u200b</a>')

            # Отправляем сообщение каждые BATCH_SIZE пользователей
            if len(link_users) == BATCH_SIZE:  # ограничение Telegram'а на 5 оповещений в одном сообщении
                batch = _format_batch(
                    prefix, ''.join(link_users), lang, chat_config.is_nickname_visible)
                await call_with_flood_wait(
                    lambda: message.reply_text(batch, parse_mode=enums.ParseMode.HTML))
                prefix = ""
                link_users = []
                await asyncio.sleep(delay)  # пауза под медленный режим чата

        # Отправляем оставшихся пользователей, если они есть
        if link_users:
            batch = _format_batch(
                prefix, ''.join(link_users), lang, chat_config.is_nickname_visible)
            await call_with_flood_wait(
                lambda: message.reply_text(batch, parse_mode=enums.ParseMode.HTML))

    except Exception as e:
        await report_error(
            app, e,
            "Ошибка при отправке ссылок на пользователей в чате",
            "Произошла ошибка при отправке ссылок в чате",
            message=message, lang=lang)
