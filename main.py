import asyncio

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from loader import app, logger, database, ADMIN_CHAT_ID
from models.models import ChatConfig
from models.utils import create_table_if_not_exists
from keyboard.keyboard_buttons import keyboard_start_ru, keyboard_start_gb, keyboard_help
from lang import get_text as _

# создаем таблицы в базе данных
database.create_tables([ChatConfig])

# словарь для хранения "замороженных" команд
frozen_commands = {}


async def get_chat_admins(message):
    """Возвращает список идентификаторов администраторов чата."""
    admins = []
    async for member in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        admins.append(member.user.id)
    return admins


async def get_chat_data(message):
    """Возвращает конфигурацию чата."""
    create_table_if_not_exists(chat_id=message.chat.id)
    chat_config = ChatConfig.get(ChatConfig.chat_id == message.chat.id)
    return chat_config


@app.on_message(filters.private)
async def start_command(client: Client, message: Message):
    """Выводит инфо сообщение с кнопкой для добавления бота в группу."""
    await message.reply_text(_('start_text'),
                             reply_markup=keyboard_start_gb, disable_web_page_preview=True,)


@app.on_message(filters.command(["help", "command"]) & filters.group)
async def help_command(client: Client, message: Message):
    """Выводит справку по всем командам."""
    chat_config = await get_chat_data(message)
    await message.reply_text(_("help_text", chat_config.language),
                             reply_markup=keyboard_help, disable_web_page_preview=True,)


@app.on_callback_query(filters.regex(r"^lang:(ru|en)(_start)?$"))
async def handle_change_lang(client: Client, query):
    """Обработчик смены языка."""
    lang = query.data.split(":")[1].split("_")[0]
    command_origin = query.data.split("_")[-1]

    if command_origin == "start":
        keybord = keyboard_start_ru if lang == "ru" else keyboard_start_gb

        await query.message.edit_text(_("start_text", lang),
                                      reply_markup=keybord, disable_web_page_preview=True,)
        return await query.answer(_("lang_changed", lang))
    else:
        # Получаем конфигурацию чата
        chat_config = await get_chat_data(query.message)
        admins = await get_chat_admins(query.message)

        if query.from_user.id not in admins:
            return await query.answer(_("only_admin_lang", lang))

        if chat_config.language == lang:
            return await query.answer(_("lang_already_set", lang))

        chat_config.language = lang
        chat_config.save()
        await query.message.edit_text(_("help_text", lang),
                                      reply_markup=keyboard_help, disable_web_page_preview=True,)
        await query.answer(_("lang_changed", lang))


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

        # Выполняем команду
        await send_user_links(message)
        # Замораживаем команду
        frozen_commands[message.chat.id] = True
        await asyncio.sleep(60)
        del frozen_commands[message.chat.id]

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        await app.send_message(ADMIN_CHAT_ID, f"ПРОИЗОШЛА ОШИБКА {e}")


async def send_user_links(message: Message):
    """Отправка сообщений с сылками на пользователей в чате."""
    # Получаем конфигурацию чата
    chat_config = await get_chat_data(message)
    lang = chat_config.language
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


@app.on_message(filters.command(["access_toggle"]) & filters.group)
async def access_toggle(client: Client, message: Message):
    """Обработчик переключения прав доступа"""
    # Получаем конфигурацию чата
    chat_config = await get_chat_data(message)
    admins = await get_chat_admins(message)
    lang = chat_config.language

    # Проверяем доступ к команде
    if message.from_user.id not in admins:
        return await message.reply(_("only_admin", lang))

    # Переключение прав доступа
    chat_config.need_access = not chat_config.need_access
    chat_config.save()

    await message.reply((_("mention_all", lang)
                         if not chat_config.need_access else _("mention_admin", lang)))


@app.on_message(filters.command(["names_visibility"]) & filters.group)
async def names_visibility_toggle(client: Client, message: Message):
    """Обработчик переключения видимости никнеймов"""
    # Получаем конфигурацию чата
    chat_config = await get_chat_data(message)
    admins = await get_chat_admins(message)
    lang = chat_config.language

    # Проверяем доступ к команде
    if message.from_user.id not in admins:
        return await message.reply(_("only_admin", lang))

    # Переключение видимости никнеймов
    chat_config.is_nickname_visible = not chat_config.is_nickname_visible
    chat_config.save()

    await message.reply(_("show_username", lang)
                        if chat_config.is_nickname_visible else _("hide_username", lang))


@app.on_message(filters.new_chat_members)
async def new_member(client: Client, message: Message):
    """Выводит меню команд при добавлении бота в группу."""
    if message.new_chat_members and message.new_chat_members[0].is_self:
        chat_id = message.chat.id

        try:
            # Получаем конфигурацию чата
            chat_config = await get_chat_data(message)
            lang = chat_config.language

            await client.send_message(chat_id, _("help_text", lang),
                                      reply_markup=keyboard_help, disable_web_page_preview=True)

        except Exception as e:
            logger.error(f"Ошибка при обработке добавления в чат: {e}")
            await client.send_message(ADMIN_CHAT_ID, f"ПРОИЗОШЛА ОШИБКА {e}")

# запускаем бота
app.run()
