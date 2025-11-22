import time
from functools import wraps
from prometheus_client import Counter, Histogram, Gauge

# Создание метрик
command_counter = Counter(
    'bot_commands_total',
    'Total number of commands used',
    ['command'])
command_errors = Counter(
    'bot_commands_errors_total',
    'Total number of command errors',
    ['command'])
command_duration = Histogram(
    'bot_command_duration_seconds',
    'Time spent processing commands',
    ['command'])
command_start_time = Gauge(
    'bot_command_start_time_seconds',
    'Timestamp when command execution started',
    ['command'])
command_end_time = Gauge(
    'bot_command_end_time_seconds',
    'Timestamp when command execution ended',
    ['command'])

# Метрики для данных из БД
language_gauge = Gauge(
    'bot_chats_by_language',
    'Number of chats by language',
    ['language'])
nickname_visibility_gauge = Gauge(
    'bot_chats_by_nickname_visibility',
    'Number of chats by nickname visibility',
    ['visibility'])
groups_count_gauge = Gauge(
    'bot_groups_total',
    'Total number of groups using the bot')


def initialize_metrics():
    """Инициализирует метрики с нулевыми значениями для всех команд"""
    commands = [
        'start', 'help', 'everyone', 'access_toggle', 'change_lang',
        'names_visibility', 'new_chat_member'
    ]

    # Инициализируем гистограмму длительности команд
    for command in commands:
        command_duration.labels(command=command).observe(0.0001)

    # Инициализируем метрики для данных из БД с нулевыми значениями
    language_gauge.labels(language='en').set(0)
    language_gauge.labels(language='ru').set(0)
    nickname_visibility_gauge.labels(visibility=0).set(0)
    nickname_visibility_gauge.labels(visibility=1).set(0)
    groups_count_gauge.set(0)


def update_database_metrics():
    """Обновляет метрики из базы данных"""
    try:
        from models.models import ChatConfig
        from loader import database

        if database.is_closed():
            database.connect()

        # Подсчитываем чаты по языкам
        for lang in ['en', 'ru']:
            count = ChatConfig.select().where(
                ChatConfig.language == lang).count()
            language_gauge.labels(language=lang).set(count)

        # Подсчитываем чаты по видимости никнеймов
        for value in [0, 1]:
            count = ChatConfig.select().where(
                ChatConfig.is_nickname_visible == value).count()
            nickname_visibility_gauge.labels(visibility=value).set(count)

        # Подсчитываем количество групп (чаты с chat_id < 0 - это группы)
        groups_count = ChatConfig.select().where(
            ChatConfig.chat_id < 0).count()
        groups_count_gauge.set(groups_count)

    except Exception as e:
        import logging
        logging.getLogger('monitoring').error(
            f"Error updating database metrics: {e}", exc_info=True)


def track_command(command_name):
    """Декоратор для отслеживания использования команд и их длительности

    ВАЖНО: В Pyrogram декораторы применяются снизу вверх!
    Поэтому этот декоратор должен быть ПОД @app.on_message:

    @app.on_message(filters.command("start"))
    @track_command("start")
    async def start_command(...):
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message_or_query):
            start_time = time.time()
            start_timestamp = time.time()

            try:
                command_counter.labels(command=command_name).inc()
                command_start_time.labels(
                    command=command_name).set(start_timestamp)
                result = await func(client, message_or_query)
                end_timestamp = time.time()
                command_end_time.labels(
                    command=command_name).set(end_timestamp)
                return result
            except Exception:
                command_errors.labels(command=command_name).inc()
                end_timestamp = time.time()
                command_end_time.labels(
                    command=command_name).set(end_timestamp)
                raise
            finally:
                duration = time.time() - start_time
                command_duration.labels(
                    command=command_name).observe(duration)

        return wrapper
    return decorator
