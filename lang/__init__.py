from importlib import import_module


def get_lexicon(lang):
    """возвращает словарь лексикона для указанного языка"""
    try:
        lexicon_module = import_module(f'lang.{lang}')
        return getattr(lexicon_module, f'LEXICON_{lang.upper()}')
    except ModuleNotFoundError:
        return {}  # Возвращаем пустой словарь, если язык не найден


def get_text(key, lang):
    """получаем текст на основе языка пользователя"""
    lexicon = get_lexicon(lang)
    if lang == 'ru':
        txt = lexicon.get(key, key)
    else:  # en - язык по умолчанию
        txt = lexicon.get(key, key)
    return txt
