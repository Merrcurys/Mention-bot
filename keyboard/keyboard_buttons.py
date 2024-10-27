from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_start = [
    [InlineKeyboardButton(text="Добавить в группу / Add to a group",
                          url="https://t.me/fast_mention_bot?startgroup=")]
]

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
