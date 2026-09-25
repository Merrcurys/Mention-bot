import logging
from pathlib import Path

from peewee import SqliteDatabase
from decouple import config
from pyrogram import Client
from pyrogram.types import LinkPreviewOptions


# Получение конфигурационных переменных из .env файла
API_TOKEN = config("API_TOKEN")
API_ID = config("API_ID")
API_HASH = config("API_HASH")
ADMIN_CHAT_ID = int(config("ADMIN_CHAT_ID"))

DIR = Path(__file__).absolute().parent

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{DIR}/logs.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Создание экземпляра бота и диспетчера для обработки сообщений
# Превью ссылок отключено глобально (disable_web_page_preview устарел в Kurigram)
app = Client(
    "bot",
    api_hash=API_HASH,
    api_id=API_ID,
    bot_token=API_TOKEN,
    link_preview_options=LinkPreviewOptions(is_disabled=True),
)

# Инициализация экземпляра базы данных
database = SqliteDatabase(
    "database.sqlite3",
    pragmas={"foreign_keys": 1},
)
