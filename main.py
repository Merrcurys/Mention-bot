from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatType
from telethon import TelegramClient
from db_handler import return_users_db, reg_users_db, delete_users_db

API_TOKEN = ""  # Ваш токен бота
API_ID = 0 # Ваш API_ID бота
API_HASH = ""  # Ваш API_ID хэш

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# * Команда /help
@dp.message_handler(commands='help', chat_type=ChatType.SUPERGROUP)
async def help_command(message: types.Message):
    help_text = ('Доступные команды:\n'
                 '/help - показать доступные команды\n'
                 '/all - тегнуть всех пользователей\n')
    await message.reply(help_text)


# * Команда /all
@dp.message_handler(commands='all', chat_type=ChatType.SUPERGROUP)
async def all_users(message: types.Message):

    if not return_users_db(message["chat"]["id"]):
        await reg_users(message)

    link_users = list()

    for i in return_users_db(message["chat"]["id"]):
        user = await bot.get_chat_member(chat_id=message.chat.id, user_id=i)
        link_users.append(
            f'<a href="tg://user?id={i}">{user.user.full_name}</a>')
    await message.reply(f"Важная информация!\n\n{', '.join(link_users)}", parse_mode="HTML")


async def reg_users(message):
    try:
        client = TelegramClient('bot', API_ID, API_HASH)
        async with client:
            objects_members, all_members = [], []
            objects_members = await client.get_participants(message["chat"]["id"], aggressive=True)
            for member in objects_members:
                if member.id != 6517195165:
                    all_members.append(member.id)
            reg_users_db(message["chat"]["id"], all_members)
    except:
        await message.reply("Произошла ошибка!")


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def get_new_chat_member_id(message: types.Message):

    new_member_id = list()
    if message.new_chat_members[-1].id != 6517195165:
        new_member_id.append(message.new_chat_members[-1].id)
        reg_users_db(message["chat"]["id"], new_member_id)


@dp.message_handler(content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
async def remove_left_chat_member_id(message: types.Message):
    left_member_id = list()
    left_member_id.append(message.left_chat_member.id)
    delete_users_db(message["chat"]["id"], left_member_id)

# * Вывод кода в тг
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
