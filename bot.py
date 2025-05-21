from loader import app, database
from models.models import ChatConfig

# Импортируем все обработчики
from handlers import *

# Создаем таблицы в базе данных
database.create_tables([ChatConfig])

# Запускаем бота
app.run()
