from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_start_ru = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="Добавить в группу",
                              url="https://t.me/fast_mention_bot?startgroup=")],
        [InlineKeyboardButton(
            text="🇬🇧 English", callback_data="lang:en_start")]
    ]
)

keyboard_start_gb = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="Add to a group",
                              url="https://t.me/fast_mention_bot?startgroup=")],
        [InlineKeyboardButton(
            text="🇷🇺 Русский", callback_data="lang:ru_start")]
    ]
)

keyboard_help = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="🇷🇺 Русский", callback_data="lang:ru"
            ),
            InlineKeyboardButton(
                text="🇬🇧 English", callback_data="lang:en"
            ),
        ]
    ]
)
