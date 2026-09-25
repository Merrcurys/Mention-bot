import asyncio
import time
from pyrogram import Client, filters
from pyrogram.types import Message

from loader import app
from lang import get_text as _
from utils.errors import call_with_flood_wait, report_error
from utils.get_admins import get_chat_admins
from utils.get_data import get_chat_data
from utils.sender import get_sender_id, is_sender_admin


# chat_id -> время (monotonic), до которого команда недоступна
frozen_commands = {}
FROZEN_SECONDS = 60


def _is_frozen(chat_id: int) -> bool:
    until = frozen_commands.get(chat_id)
    return until is not None and time.monotonic() < until


def _freeze(chat_id: int) -> None:
    now = time.monotonic()
    for expired in [cid for cid, until in frozen_commands.items() if until <= now]:
        frozen_commands.pop(expired, None)
    frozen_commands[chat_id] = now + FROZEN_SECONDS


@app.on_message(filters.command(["all", "here", "everyone"]) & filters.group)
async def everyone_command(client: Client, message: Message):
    """Обработчик команды для оповещения всех пользователей."""
    try:
        # Получаем конфигурацию чата
        chat_config = await get_chat_data(message)
        admins = await get_chat_admins(message)
        lang = chat_config.language

        # Проверяем доступ к команде
        if chat_config.need_access and not is_sender_admin(message, admins):
            return await message.reply(_("only_admin", lang))

        # Проверяем количество пользователей
        if len([member async for member in app.get_chat_members(message.chat.id)]) > 75:
            return await message.reply(_("many_users", lang))

        # Проверяем заморожена ли команда
        if _is_frozen(message.chat.id):
            return await message.reply(_("spam_control", lang))

        # Замораживаем сразу, до отправки, чтобы параллельные /all не дублировались
        _freeze(message.chat.id)
        await send_user_links(message, chat_config, lang)
    except Exception as e:
        await report_error(
            app, e,
            "Ошибка при выполнении команды /all в чате",
            "Произошла ошибка при выполнении /all в чате")


async def send_user_links(message: Message, chat_config, lang):
    """Отправка сообщений с сылками на пользователей в чате."""
    try:
        link_users = []
        users_found = False
        sender_id = get_sender_id(message)

        # Получаем список пользователей этого чата
        async for user in app.get_chat_members(message.chat.id):
            # Пропускаем ботов, удаленных пользователей и самого отправителя сообщения
            if user.user.is_bot or user.user.is_deleted or sender_id == user.user.id:
                continue

            # Указываем что сообщение было выведено хотя бы 1 раз
            users_found = True

            # Формируем ссылку на пользователя
            if chat_config.is_nickname_visible:
                # Используем юзернейм, если он есть, иначе имя пользователя для ссылки
                link_users.append(
                    f"[@{user.user.username or user.user.first_name}, ](tg://user?id={user.user.id})")
            else:
                # Используем невидимый символ (U+200b) для скрытия имени пользователя
                link_users.append(f"[​](tg://user?id={user.user.id})")

            # Отправляем сообщение каждые 5 пользователей
            if len(link_users) == 5:  # ограничение Telegram'а на 5 оповещений в одном сообщении
                batch = f"{_('all_info', lang)}{''.join(link_users)}"
                await call_with_flood_wait(lambda: message.reply(batch))
                link_users = []
                await asyncio.sleep(1)  # мягкий троттлинг, чтобы реже ловить FLOOD_WAIT

        # Отправляем оставшихся пользователей, если они есть
        if link_users:
            batch = f"{_('all_info', lang)}{''.join(link_users)}"
            await call_with_flood_wait(lambda: message.reply(batch))

        # Отправляем сообщение, если пользователей не было найдено
        elif not users_found:
            await call_with_flood_wait(lambda: message.reply(_('no_users_found', lang)))

    except Exception as e:
        await report_error(
            app, e,
            "Ошибка при отправке ссылок на пользователей в чате",
            "Произошла ошибка при отправке ссылок в чате")
