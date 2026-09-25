import logging
from importlib import import_module

logger = logging.getLogger(__name__)

SUPPORTED_LANGS = ("ru", "en")
DEFAULT_LANG = "en"


def get_lang_by_code(language_code) -> str:
    """Определяет язык бота по языку клиента Telegram.

    ``language_code`` — IETF-тег (например, ``ru``, ``ru-RU``, ``en-US``).
    Если язык не определён или не поддерживается — английский.
    """
    if not language_code:
        return DEFAULT_LANG

    primary = str(language_code).replace("_", "-").split("-")[0].lower()
    return primary if primary in SUPPORTED_LANGS else DEFAULT_LANG


def get_lexicon(lang):
    """Возвращает словарь лексикона для указанного языка."""
    try:
        lexicon_module = import_module(f'lang.{lang}')
    except ModuleNotFoundError:
        logger.warning("Лексикон для языка '%s' не найден", lang)
        return {}

    return getattr(lexicon_module, f'LEXICON_{lang.upper()}', {})


def get_text(key, lang="en"):
    """Получаем текст на основе языка пользователя."""
    lexicon = get_lexicon(lang)
    if key not in lexicon:
        logger.warning("Нет ключа '%s' для языка '%s'", key, lang)
        return key
    return lexicon[key]


def get_help_text(chat_config) -> str:
    """Собирает текст справки по текущим настройкам чата."""
    lang = chat_config.language
    help_3_command = "help_text_3_only" if chat_config.need_access else "help_text_3_many"
    help_4_command = "help_text_4_show" if chat_config.is_nickname_visible else "help_text_4_hide"

    return (
        get_text("help_text_start", lang)
        + get_text(help_3_command, lang)
        + get_text(help_4_command, lang)
        + get_text("help_text_end", lang)
    )
