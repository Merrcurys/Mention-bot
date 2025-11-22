import logging
import time
from pathlib import Path
from threading import Thread

from peewee import SqliteDatabase
from decouple import config
from pyrogram import Client
from prometheus_client import start_http_server
from utils.monitoring import initialize_metrics, update_database_metrics


# получение конфигурационных переменных из .env файла
API_TOKEN = config("API_TOKEN")
API_ID = config("API_ID")
API_HASH = config("API_HASH")
ADMIN_CHAT_ID = int(config("ADMIN_CHAT_ID"))

DIR = Path(__file__).absolute().parent

# настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{DIR}/logs.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# создание экземпляра бота и диспетчера для обработки сообщений
app = Client("bot", api_hash=API_HASH, api_id=API_ID, bot_token=API_TOKEN)

# инициализация экземпляра базы данных
database = SqliteDatabase(
    "database.sqlite3",
    pragmas={"foreign_keys": 1},
)

# Start Prometheus metrics server in a separate thread


def start_metrics_server():
    start_http_server(8001)


def update_metrics_periodically():
    """Периодически обновляет метрики из БД"""
    time.sleep(2)  # Ждем инициализации БД
    while True:
        try:
            update_database_metrics()
            time.sleep(60)  # Обновляем каждую минуту
        except Exception as e:
            logger.error(f"Error in metrics update thread: {e}")
            time.sleep(60)


metrics_thread = Thread(target=start_metrics_server, daemon=True)
metrics_thread.start()

# Поток для периодического обновления метрик из БД
metrics_update_thread = Thread(
    target=update_metrics_periodically, daemon=True)
metrics_update_thread.start()

# Инициализируем метрики с нулевыми значениями после запуска сервера
# Это нужно, чтобы метрики были видны в Prometheus
# даже до первого использования
time.sleep(0.5)  # Небольшая задержка для запуска сервера
initialize_metrics()
time.sleep(1)  # Дополнительная задержка для БД
update_database_metrics()
