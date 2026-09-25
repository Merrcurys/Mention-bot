"""Премиум-эмодзи Telegram, вынесенные отдельно от текстов.

В текстах используются плейсхолдеры вида {name}, которые подставляются
через ``str.format(**get_emoji(lang))`` в языковых файлах.
"""

PREMIUM_EMOJI = {
    "ru": {
        "header_1": "<emoji id=5287701007390746028>😀</emoji>",
        "header_2": "<emoji id=5287271536430948585>😀</emoji>",
        "header_3": "<emoji id=5287716774215689708>😀</emoji>",
        "header_4": "<emoji id=5289925796155106922>😀</emoji>",
        "header_5": "<emoji id=5287588797075170892>😀</emoji>",
        "header_6": "<emoji id=5289543758814127281>😀</emoji>",
        "header_7": "<emoji id=5287362237550307187>😀</emoji>",
        "help": "<emoji id=5287353089269966535>😀</emoji>",
        "all": "<emoji id=5287250783148976769>😀</emoji>",
        "access": "<emoji id=5287753603560252687>😀</emoji>",
        "lock_all": "<emoji id=6037496202990194718>🔒</emoji>",
        "lock_admin": "<emoji id=6037249452824072506>🔒</emoji>",
        "visibility": "<emoji id=5287257182650247240>😀</emoji>",
        "eye_visible": "<emoji id=6037397706505195857>👁</emoji>",
        "eye_hidden": "<emoji id=6037243349675544634>👁</emoji>",
        "bolt": "<emoji id=5321097148371058002>⚡️</emoji>",
    },
    "en": {
        "header_1": "<emoji id=5287630698776110505>😀</emoji>",
        "header_2": "<emoji id=5287270733272065330>😀</emoji>",
        "header_3": "<emoji id=5289509454910334424>😀</emoji>",
        "header_4": "<emoji id=5287695703106134591>😀</emoji>",
        "header_5": "<emoji id=5287627636464427992>😀</emoji>",
        "header_6": "<emoji id=5287698194187166324>😀</emoji>",
        "header_7": "<emoji id=5287762975178892826>😀</emoji>",
        "help": "<emoji id=5287353089269966535>😀</emoji>",
        "all": "<emoji id=5287250783148976769>😀</emoji>",
        "access": "<emoji id=5287753603560252687>😀</emoji>",
        "lock_all": "<emoji id=6037496202990194718>🔒</emoji>",
        "lock_admin": "<emoji id=6037249452824072506>🔒</emoji>",
        "visibility": "<emoji id=5287257182650247240>😀</emoji>",
        "eye_visible": "<emoji id=6037397706505195857>👁</emoji>",
        "eye_hidden": "<emoji id=6037243349675544634>👁</emoji>",
        "bolt": "<emoji id=5321097148371058002>⚡️</emoji>",
    },
}


def get_emoji(lang: str = "en") -> dict:
    """Возвращает набор премиум-эмодзи для указанного языка."""
    return PREMIUM_EMOJI.get(lang, PREMIUM_EMOJI["en"])
