import asyncio

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from loader import app, logger, ADMIN_CHAT_ID, database
from models.models import ChatConfig
from models.utils import create_table_if_not_exists

# создаем таблицы в базе данных
database.create_tables([ChatConfig])

# словарь для хранения "замороженных" команд
frozen_commands = {}

# Функция для получения администраторов чата
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
@app.on_message(
    filters.command(["help", "start", "command"]) & (filters.group | filters.private)
)
async def help_command(client: Client, message: Message):
    help_text = """
———СПИСОК КОМАНД———

1. /help, /command - справка по всем командам.

2. /all, /here, /everyone - позвать всех пользователей. 

3. /access_toggle - тумблер прав доступа к оповещениям.

4. /names_visibility - тумблер для видимости имен при оповещении.

тех.поддержка - @merrcurys
version: 3.1
    """
    await message.reply_text(help_text)


# --------функция оповещения--------
@app.on_message(filters.command(["all", "here", "everyone"]) & filters.group)
async def call_all_users(client: Client, message: Message):
    try:
        create_table_if_not_exists(chat_id=message.chat.id)
        admins = await get_chat_admins(message)
        chat_config = ChatConfig.get(ChatConfig.chat_id == message.chat.id)

        # проверяем, имеет ли пользователь доступ или является администратором
        if not chat_config.need_access or message.from_user.id in admins:
            # проверяем, что пользователей в чате не больше 75
            members = [member async for member in app.get_chat_members(message.chat.id)]
            if len(members) <= 75:
                if message.chat.id in frozen_commands:
                    await message.reply("Эту команду можно использовать только один раз в минуту.")
                else:
                    # выполняем команду и замораживаем её на 60 секунд
                    await send_user_links(message)
                    frozen_commands[message.chat.id] = True
                    await asyncio.sleep(60)
                    del frozen_commands[message.chat.id]
            else:
                await message.reply("Эту команду можно использовать только если в чате не больше 75 пользователей.")
        else:
            await message.reply("Только администраторы могут использовать данную команду.")
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
        if ChatConfig.get(ChatConfig.chat_id == message.chat.id).is_nickname_visible:
            link_users.append(
                # создаем ссылку на пользователя с его юзернеймом или с именем
                f"[@{user.user.username or user.user.first_name}, ](tg://user?id={user.user.id})"
            )
        else:
            # создаем ссылку на пользователя с использованием специального символа U+200b (невидимый символ)
            link_users.append(f"[​](tg://user?id={user.user.id})")

        # отправляем сообщение каждые 5 пользователей (ограничение телеграмма на 5 ссылок в 1 сообщении)
        if len(link_users) == 5:
            await message.reply(
                f"Важная информация!{''.join(link_users)}",
                parse_mode=enums.ParseMode.MARKDOWN,
            )
            link_users = []

    # отправляем оставшихся пользователей, если они есть
    if link_users:
        await message.reply(
            f"Важная информация!{''.join(link_users)}",
            parse_mode=enums.ParseMode.MARKDOWN,
        )


# --------функция переключения прав доступа--------
@app.on_message(filters.command(["access_toggle"]) & filters.group)
async def access_toggle(client: Client, message: Message):
    create_table_if_not_exists(chat_id=message.chat.id)

    # получаем список администраторов чата
    admins = await get_chat_admins(message)
    chat_config = ChatConfig.get(ChatConfig.chat_id == message.chat.id)

    if message.from_user.id in admins:
        chat_config.need_access = not chat_config.need_access
        chat_config.save()

        text = (
            "Упоминать участников чата теперь могут все."
            if not chat_config.need_access
            else "Упоминать участников чата теперь могут только администраторы."
        )
        await message.reply(text)

    else:
        # отправляем сообщение об ошибке, если отправитель не является администратором
        await message.reply("Только администраторы могут использовать данную команду.")


# --------функция переключения видимости имен--------
@app.on_message(filters.command(["names_visibility"]) & filters.group)
async def names_visibility_toggle(client: Client, message: Message):
    create_table_if_not_exists(chat_id=message.chat.id)

    # получаем список администраторов чата
    admins = await get_chat_admins(message)
    chat_config = ChatConfig.get(ChatConfig.chat_id == message.chat.id)

    if message.from_user.id in admins:
        chat_config.is_nickname_visible = not chat_config.is_nickname_visible
        chat_config.save()

        text = (
            "При упоминание участников чата юзернеймы теперь отображаются."
            if chat_config.is_nickname_visible
            else "При упоминание участников чата юзернеймы теперь скрыты."
        )
        await message.reply(text)

    else:
        # отправляем сообщение об ошибке, если отправитель не является администратором
        await message.reply("Только администраторы могут использовать данную команду.")


# запускаем бота
app.run()
