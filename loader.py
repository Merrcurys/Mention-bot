import asyncio
import logging

from pyrogram import Client, filters, enums
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