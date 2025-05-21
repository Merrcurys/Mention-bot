import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message

from loader import app, logger, ADMIN_CHAT_ID
from lang import get_text as _
from utils.get_admins import get_chat_admins
from utils.get_data import get_chat_data

# словарь для хранения "замороженных" команд
frozen_commands = {}


@app.on_message(filters.command(["all", "here", "everyone"]) & filters.group)
async def everyone_command(client: Client, message: Message):
    """Обработчик команды для оповещения всех пользователей."""
    try:
        # Получаем конфигурацию чата
        chat_config = await get_chat_data(message)
        admins = await get_chat_admins(message)
        lang = chat_config.language

        # Проверяем доступ к команде
        if chat_config.need_access and message.from_user.id not in admins:
            return await message.reply(_("only_admin", lang))

        # Проверяем количество пользователей
        if len([member async for member in app.get_chat_members(message.chat.id)]) > 75:
            return await message.reply(_("many_users", lang))

        # Проверяем заморожена ли команда
        if message.chat.id in frozen_commands:
            return await message.reply(_("spam_control", lang))

        # Выполняем команду и замораживаем на 60 секунд
        await send_user_links(message, chat_config, lang)
        frozen_commands[message.chat.id] = True
        await asyncio.sleep(60)
        del frozen_commands[message.chat.id]
    except Exception as e:
        logger.error(
            f"Ошибка при выполнении команды /all в чате: {e}", exc_info=True)
        await app.send_message(ADMIN_CHAT_ID, f"Произошла ошибка при выполнении /all в чате: {e}")


async def send_user_links(message: Message, chat_config, lang):
    """Отправка сообщений с сылками на пользователей в чате."""
    try:
        link_users = []
        users_found = False

        # Получаем список пользователей этого чата
        async for user in app.get_chat_members(message.chat.id):
            # Пропускаем ботов, удаленных пользователей и самого отправителя сообщения
            if user.user.is_bot or user.user.is_deleted or message.from_user.id == user.user.id:
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
                await message.reply(f"{_('all_info', lang)}{''.join(link_users)}", parse_mode=enums.ParseMode.MARKDOWN,)
                link_users = []

        # Отправляем оставшихся пользователей, если они есть
        if link_users:
            await message.reply(f"{_('all_info', lang)}{''.join(link_users)}", parse_mode=enums.ParseMode.MARKDOWN,)

        # Отправляем сообщение, если пользователей не было найдено
        elif not users_found:
            await message.reply(_('no_users_found', lang))

    except Exception as e:
        logger.error(
            f"Ошибка при отправке ссылок на пользователей в чате: {e}", exc_info=True)
        await app.send_message(ADMIN_CHAT_ID, f"Произошла ошибка при отправке ссылок в чате: {e}")
