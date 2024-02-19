from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatType
from telethon import TelegramClient
from database import BotDatabase
from decouple import config
import asyncio
import logging

# получение конфигурационных переменных из .env файла
API_TOKEN = config('API_TOKEN')
BOT_ID = int(config('BOT_ID'))
API_ID = config('API_ID')
API_HASH = config('API_HASH')
ADMIN_CHAT_ID = int(config('ADMIN_CHAT_ID'))

# настройка логгирования
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# создание экземпляра бота и диспетчера для обработки сообщений
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# инициализация экземпляра базы данных
db = BotDatabase()

# словарь для хранения "замороженных" команд
frozen_commands = {}


# --------функция помощи--------
@dp.message_handler(commands=["help", "start", "command"], chat_type=[ChatType.SUPERGROUP, ChatType.GROUP, ChatType.PRIVATE])
async def help_command(message: types.Message):
    help_text = (
        """
———СПИСОК КОМАНД———

1. /start, /command, /help - справка по всем командам.

2. /all, /here, /everyone – позвать всех пользователей. 

3. /mentions_toggle - тумблер прав доступа к оповещениям.

тех.поддержка - @merrcurys
version: 2.0
    """)
    await message.reply(help_text)


# --------функция оповещения--------
# обработчик команд для оповещения всех пользователей
@dp.message_handler(commands=["all", "here", "everyone"], chat_type=[ChatType.SUPERGROUP, ChatType.GROUP])
async def call_all_users(message: types.Message):
    # проверяем есть ли поользователи в данном чате в базе данных
    if not db.get_all_users(message.chat.id):
        await register_users_in_chat(message)

    # получаем список администраторов чата
    chat_admins = await bot.get_chat_administrators(message.chat.id)
    admins = [admin.user.id for admin in chat_admins]

    # проверяем наличие прав доступа к команде
    if db.get_position_tb(message.chat.id)[0] or message.from_user.id in admins:
        if message.chat.id in frozen_commands:
            await message.reply("Эту команду нельзя использовать чаще чем один раз в минуту.")
        else:
            await send_user_links(message)
            frozen_commands[message.chat.id] = True
            await asyncio.sleep(60)  # Задержка в 60 секунд
            del frozen_commands[message.chat.id]
    else:
        await message.reply("Только администраторы могут использовать данную команду.")


# отправка сообщений с оповещением пользователей
async def send_user_links(message):
    link_users = []

    # получаем список пользователей из базы данных для данного чата и формируем ссылки на них
    for user_id in db.get_all_users(message.chat.id):
        user = await bot.get_chat_member(chat_id=message.chat.id, user_id=user_id)
        # создаем ссылку на пользователя с использованием специального символа U+200b (невидимый символ)
        link_users.append(f"[​](tg://user?id={user.user.id})")

        # отправляем сообщение каждые 5 пользователей
        if len(link_users) == 5:
            await message.reply(f"Важная информация!{''.join(link_users)}", parse_mode="Markdown")
            link_users = []

    # отправляем оставшихся пользователей, если они есть
    if link_users:
        await message.reply(f"Важная информация!{''.join(link_users)}", parse_mode="Markdown")


# добавление пользователей в базу данных
async def register_users_in_chat(message):
    try:
        db.add_chat_db(message.chat.id)
        client = TelegramClient('bot', API_ID, API_HASH)

        async with client:
            # получаем всех участников чата, исключая ботов
            objects_members = await client.get_participants(message.chat.id, aggressive=True)
            all_members = [member.id for member in objects_members if not member.bot]

            db.add_users_db(message.chat.id, all_members)

    except Exception as e:
        await message.reply("Произошла ошибка! Попробуйте еще раз.")


# --------тумблер--------
# обработчик команды для переключения прав доступа к оповещениям
@dp.message_handler(commands='mentions_toggle', chat_type=[ChatType.SUPERGROUP, ChatType.GROUP])
async def toggle_mention_notifications(message: types.Message):
    # проверяем есть ли поользователи в данном чате в базе данных
    if not db.get_all_users(message.chat.id):
        await register_users_in_chat(message)

    admins = await bot.get_chat_administrators(message.chat.id)
    toggle = db.get_position_tb(message.chat.id)[0]
    admins_id = [admin.user.id for admin in admins]

    # проверяем, является ли отправитель сообщения администратором
    if message.from_user.id in admins_id:
        toggle = not toggle
        db.update_mentions_tb(message.chat.id, toggle)

        text = "Упоминать участников чата теперь могут все." if toggle else "Упоминать участников чата теперь могут только администраторы."
        await message.reply(text)

    else:
        # отправляем сообщение об ошибке, если отправитель не является администратором
        await message.reply("Только администраторы могут использовать данную команду.")


# --------функции добавления/удаления участников--------
# обработчик новых участников чата
@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def handle_new_chat_members(message: types.Message):
    new_members = message.new_chat_members

    if BOT_ID == new_members[-1].id:
        # добавление чата и его пользователей в базу данных
        db.add_chat_db(message.chat.id)
        await register_users_in_chat(message)

    else:
        # добавление нового пользователя в базу данных
        if not new_members[-1]["is_bot"]:
            db.add_users_db(message.chat.id, list(str(new_members[-1].id).split(" ")))

    members_count = len(db.get_all_users(message.chat.id))

    # проверка количества участников и выход из чата, если их слишком много
    if members_count > 75:
        await message.reply("В чате слишком много участников, для стабильной работы бота нужно не больше 75 пользователей.")
        await bot.leave_chat(message.chat.id)


# обработчик ушедших участников чата
@dp.message_handler(content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
async def handle_left_chat_member(message: types.Message):
    left_member_id = message.left_chat_member.id
    chat_id = message.chat.id

    if BOT_ID == left_member_id:
        # удалить всех пользователей чата и информацию о чате, если ушел бот
        all_users = db.get_all_users(chat_id)
        db.del_users_from_chat_db(chat_id, all_users)
        db.del_chat_db(chat_id)
    else:
        # удалить ушедшего участника из базы данных чата
        left_member_id_list = list(map(int, str(left_member_id).split(" ")))
        db.del_users_from_chat_db(chat_id, left_member_id_list)


# обработчик ошибок
async def error_handler(update, exception):
    logger.error(f'Update {update} caused error: {exception}')
    # отправляем сообщение об ошибке в админский чат
    await bot.send_message(ADMIN_CHAT_ID, f'ПРОИЗОШЛА ОШИБКА\n\n{update}\n\n<{exception}>')


dp.register_errors_handler(error_handler)  # Регистрация обработчика ошибок

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
