import asyncio

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from loader import app, db, logger, ADMIN_CHAT_ID


# словарь для хранения "замороженных" команд
frozen_commands = {}


@app.on_message(
    filters.command(["help", "start", "command"]) & (filters.group | filters.private)
)
async def help_command(client: Client, message: Message):
    help_text = """
———СПИСОК КОМАНД———

1. /start, /command, /help - справка по всем командам.

2. /all, /here, /everyone – позвать всех пользователей. 

3. /mentions_toggle - тумблер прав доступа к оповещениям.

тех.поддержка - @merrcurys
version: 3.0
    """
    await message.reply_text(help_text)


# --------функция оповещения--------
# обработчик команд для оповещения всех пользователей
@app.on_message(
    filters.command(["all", "here", "everyone"]) & (filters.group | filters.private)
)
async def call_all_users(client: Client, message: Message):
    # получаем список администраторов чата
    chat_admins = [
        admin
        async for admin in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        )
    ]
    admins = [admin.user.id for admin in chat_admins]

    # проверяем наличие прав доступа к команде
    if db.get_position_tb(message.chat.id)[0] or message.from_user.id in admins:
        if message.chat.id in frozen_commands:
            await message.reply(
                "Эту команду нельзя использовать чаще чем один раз в минуту."
            )
        else:
            await send_user_links(message)
            frozen_commands[message.chat.id] = True
            await asyncio.sleep(60)  # Задержка в 60 секунд
            del frozen_commands[message.chat.id]
    else:
        await message.reply("Только администраторы могут использовать данную команду.")


async def send_user_links(message: Message):
    link_users = []

    # получаем список пользователей из базы данных для данного чата и формируем ссылки на них
    async for user in app.get_chat_members(message.chat.id):
        # создаем ссылку на пользователя с использованием специального символа U+200b (невидимый символ)
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


@app.on_message(filters.command(["mentions_toggle"]) & filters.group)
async def toggle_mention_notifications(client: Client, message: Message):
    admins = [
        admin
        async for admin in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        )
    ]
    toggle = db.get_position_tb(message.chat.id)[0]
    admins_id = [admin.user.id for admin in admins]

    if message.from_user.id in admins_id:
        toggle = not toggle
        db.update_mentions_tb(message.chat.id, toggle)

        text = (
            "Упоминать участников чата теперь могут все."
            if toggle
            else "Упоминать участников чата теперь могут только администраторы."
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
