import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from database import BotDatabase
from decouple import config



# получение конфигурационных переменных из .env файла
API_TOKEN = config("API_TOKEN")
BOT_ID = int(config("BOT_ID"))
API_ID = config("API_ID")
API_HASH = config("API_HASH")
ADMIN_CHAT_ID = int(config("ADMIN_CHAT_ID"))

# настройка логгирования
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# создание экземпляра бота и диспетчера для обработки сообщений
app = Client("bot", api_hash=API_HASH, api_id=API_ID, bot_token=API_TOKEN)

# инициализация экземпляра базы данных
db = BotDatabase()

# словарь для хранения "замороженных" команд
frozen_commands = {}


@app.on_message(filters.command(["help", "start", "command"]) & (filters.group | filters.private))
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


app.run()