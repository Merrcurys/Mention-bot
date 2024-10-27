import asyncio

from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from loader import app, logger, ADMIN_CHAT_ID, database
from models.models import ChatConfig
from models.utils import create_table_if_not_exists
from lang import get_text as _

# создаем таблицы в базе данных
database.create_tables([ChatConfig])

# словарь для хранения "замороженных" команд
frozen_commands = {}


# функция для получения администраторов чата
async def get_chat_admins(message):
    admins = [
        admin
        async for admin in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        )
    ]
    admins_id = [admin.user.id for admin in admins]
    return admins_id


# --------функция справки--------
@app.on_message(filters.command(["help", "command"]) & filters.group)
async def help_command(client: Client, message: Message):
    user_language = message.from_user.language_code

    create_table_if_not_exists(chat_id=message.chat.id)
    chat_config = ChatConfig.get(ChatConfig.chat_id == message.chat.id)
    chat_config.language

    # Создаем кнопки
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🇷🇺 Русский", callback_data="lang:ru"
                ),
                InlineKeyboardButton(
                    text="🇬🇧 English", callback_data="lang:en"
                ),
            ]
        ]
    )

    await message.reply_text(
        _("help_text", chat_config.language),
        reply_markup=keyboard,
    )


# --------обработка нажатий на кнопки--------
@app.on_callback_query(filters.regex(r"^lang:"))
async def handle_lang_change(client: Client, query):
    lang = query.data.split(":")[1]

    create_table_if_not_exists(chat_id=query.message.chat.id)
    chat_config = ChatConfig.get(ChatConfig.chat_id == query.message.chat.id)
    if chat_config.language != lang:
        chat_config.language = lang
        chat_config.save()
        await query.message.edit_text(
            _("help_text", lang),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🇷🇺 Русский", callback_data="lang:ru"
                        ),
                        InlineKeyboardButton(
                            text="🇬🇧 English", callback_data="lang:en"
                        ),
                    ]
                ]
            ),
        )


# --------функция справки--------
@app.on_message(filters.command(["start"]) & filters.private)
async def help_command(client: Client, message: Message):
    user_language = message.from_user.language_code
    await message.reply_text(_('help_text', user_language))


# --------функция оповещения--------
@app.on_message(filters.command(["all", "here", "everyone"]) & filters.group)
async def call_all_users(client: Client, message: Message):
    try:
        # Получаем конфигурацию чата
        create_table_if_not_exists(chat_id=message.chat.id)
        admins = await get_chat_admins(message)
        chat_config = ChatConfig.get(ChatConfig.chat_id == message.chat.id)
        lang = chat_config.language

        # проверяем, имеет ли пользователь доступ или является администратором
        if not chat_config.need_access or message.from_user.id in admins:
            # проверяем, что пользователей в чате не больше 75
            members = [member async for member in app.get_chat_members(message.chat.id)]
            if len(members) <= 75:
                if message.chat.id in frozen_commands:
                    await message.reply(_("spam_control", lang))
                else:
                    # выполняем команду и замораживаем её на 60 секунд
                    await send_user_links(message)
                    frozen_commands[message.chat.id] = True
                    await asyncio.sleep(60)
                    del frozen_commands[message.chat.id]
            else:
                await message.reply(_("many_users", lang))
        else:
            await message.reply(_("only_admin", lang))
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        await app.send_message(ADMIN_CHAT_ID, f"ПРОИЗОШЛА ОШИБКА {e}")


# функция отправки ссылок пользователям
async def send_user_links(message: Message):
    link_users = []

    # получаем список пользователей этого чата и формируем ссылки на них
    async for user in app.get_chat_members(message.chat.id):
        if user.user.is_bot:
            continue

        chat_config = ChatConfig.get(ChatConfig.chat_id == message.chat.id)
        lang = chat_config.language

        if chat_config.is_nickname_visible:
            link_users.append(
                # создаем ссылку на пользователя с его юзернеймом или с именем
                f"[@{user.user.username or user.user.first_name}, ](tg://user?id={
                    user.user.id})"
            )
        else:
            # создаем ссылку на пользователя с использованием специального символа U+200b (невидимый символ)
            link_users.append(f"[​](tg://user?id={user.user.id})")

        # отправляем сообщение каждые 5 пользователей (ограничение телеграмма на 5 ссылок в 1 сообщении)
        if len(link_users) == 5:
            await message.reply(
                f"{_('all_info', lang)}{''.join(link_users)}",
                parse_mode=enums.ParseMode.MARKDOWN,
            )
            link_users = []

    # отправляем оставшихся пользователей, если они есть
    if link_users:
        await message.reply(
            f"{_('all_info', lang)}{''.join(link_users)}",
            parse_mode=enums.ParseMode.MARKDOWN,
        )


# --------функция переключения прав доступа--------
@app.on_message(filters.command(["access_toggle"]) & filters.group)
async def access_toggle(client: Client, message: Message):
    # Получаем конфигурацию чата
    create_table_if_not_exists(chat_id=message.chat.id)
    admins = await get_chat_admins(message)
    chat_config = ChatConfig.get(ChatConfig.chat_id == message.chat.id)
    lang = chat_config.language

    if message.from_user.id in admins:
        chat_config.need_access = not chat_config.need_access
        chat_config.save()

        text = (
            _("mention_all", lang)
            if not chat_config.need_access
            else _("mention_admin", lang)
        )
        await message.reply(text)

    else:
        # отправляем сообщение об ошибке, если отправитель не является администратором
        await message.reply(_("only_admin", lang))


# --------функция переключения видимости имен--------
@app.on_message(filters.command(["names_visibility"]) & filters.group)
async def names_visibility_toggle(client: Client, message: Message):
    # Получаем конфигурацию чата
    create_table_if_not_exists(chat_id=message.chat.id)
    admins = await get_chat_admins(message)
    chat_config = ChatConfig.get(ChatConfig.chat_id == message.chat.id)
    lang = chat_config.language

    if message.from_user.id in admins:
        chat_config.is_nickname_visible = not chat_config.is_nickname_visible
        chat_config.save()

        text = (
            _("show_username", lang)
            if chat_config.is_nickname_visible
            else _("hide_username", lang)
        )
        await message.reply(text)

    else:
        # отправляем сообщение об ошибке, если отправитель не является администратором
        await message.reply(_("only_admin", lang))


# запускаем бота
app.run()
