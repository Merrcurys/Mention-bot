import asyncio

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from loader import app, logger, ADMIN_CHAT_ID, database
from models.models import ChatConfig


# словарь для хранения "замороженных" команд
database.create_tables([ChatConfig])
frozen_commands = {}


def create_table_if_not_exists(chat_id: int):
    if not ChatConfig.select().where(ChatConfig.chat_id == chat_id).exists():
        ChatConfig.create(chat_id=chat_id)


@app.on_message(
    filters.command(["help", "start", "command"]) & (filters.group | filters.private)
)
async def help_command(client: Client, message: Message):
    help_text = """
———СПИСОК КОМАНД———

1. /start, /command, /help - справка по всем командам.

2. /all, /here, /everyone – позвать всех пользователей. 

3. /access_toggle - тумблер прав доступа к оповещениям.

4. /names_visibility

тех.поддержка - @merrcurys
version: 3.0
    """
    await message.reply_text(help_text)


# --------функция оповещения--------
# обработчик команд для оповещения всех пользователей
@app.on_message(filters.command(["all", "here", "everyone"]) & filters.group)
async def call_all_users(client: Client, message: Message):
    create_table_if_not_exists(chat_id=message.chat.id)

    # получаем список администраторов чата
    chat_admins = [
        admin
        async for admin in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        )
    ]
    admins = [admin.user.id for admin in chat_admins]

    # проверяем наличие прав доступа к команде
    if (
        not ChatConfig.get(ChatConfig.chat_id == message.chat.id).need_access
        or message.from_user.id in admins
    ):
        if message.chat.id in frozen_commands:
            await message.reply(
                "Эту команду нельзя использовать чаще чем один раз в минуту."
            )
        else:
            await send_user_links(message)
            frozen_commands[message.chat.id] = True
            await asyncio.sleep(10)  # Задержка в 60 секунд
            del frozen_commands[message.chat.id]
    else:
        await message.reply("Только администраторы могут использовать данную команду.")


async def send_user_links(message: Message):
    link_users = []

    # получаем список пользователей из базы данных для данного чата и формируем ссылки на них
    async for user in app.get_chat_members(message.chat.id):
        if user.user.is_bot:
            continue
        # создаем ссылку на пользователя с использованием специального символа U+200b (невидимый символ)
        if ChatConfig.get(ChatConfig.chat_id == message.chat.id).is_nickname_visible:
            link_users.append(f"[@{user.user.username or user.user.first_name}, ](tg://user?id={user.user.id})")
        
        else:
            link_users.append(f"[​](tg://user?id={user.user.id})")

        # отправляем сообщение каждые 5 пользователей
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


@app.on_message(filters.command(["access_toggle"]) & filters.group)
async def access_toggle(client: Client, message: Message):
    create_table_if_not_exists(chat_id=message.chat.id)

    admins = [
        admin
        async for admin in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        )
    ]
    chat_config = ChatConfig.get(ChatConfig.chat_id == message.chat.id)
    admins_id = [admin.user.id for admin in admins]

    if message.from_user.id in admins_id:
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


@app.on_message(filters.command(["names_visibility"]) & filters.group)
async def names_visibility_toggle(client: Client, message: Message):
    create_table_if_not_exists(chat_id=message.chat.id)

    admins = [
        admin
        async for admin in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        )
    ]
    chat_config = ChatConfig.get(ChatConfig.chat_id == message.chat.id)
    admins_id = [admin.user.id for admin in admins]

    if message.from_user.id in admins_id:
        chat_config.is_nickname_visible = not chat_config.is_nickname_visible
        chat_config.save()

        text = (
            "Юзернеймы теперь отображаются."
            if chat_config.is_nickname_visible
            else "Юзернеймы скрыты."
        )
        await message.reply(text)

    else:
        # отправляем сообщение об ошибке, если отправитель не является администратором
        await message.reply("Только администраторы могут использовать данную команду.")


async def error_handler(update, exception):
    logger.error(f"Update {update} caused error: {exception}")
    # отправляем сообщение об ошибке в админский чат
    await app.send_message(
        ADMIN_CHAT_ID, f"ПРОИЗОШЛА ОШИБКА\n\n{update}\n\n<{exception}>"
    )


app.run()
