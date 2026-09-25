from pyrogram import Client, filters
from pyrogram.types import Message

from loader import app
from keyboard.keyboard_buttons import keyboard_help
from lang import get_help_text
from utils.errors import report_error
from utils.get_data import get_chat_data


# Ограничиваем проверку списка добавленных участников (защита от огромных апдейтов)
NEW_MEMBERS_CHECK_LIMIT = 75


@app.on_message(filters.new_chat_members)
async def adding_bot_group(client: Client, message: Message):
    """Выводит меню команд при добавлении бота в группу."""
    lang = "en"
    try:
        if message.new_chat_members and any(
            member.is_self
            for member in message.new_chat_members[:NEW_MEMBERS_CHECK_LIMIT]
        ):
            # Получаем конфигурацию чата
            chat_config = await get_chat_data(message)
            lang = chat_config.language

            await client.send_message(message.chat.id, get_help_text(chat_config),
                                      reply_markup=keyboard_help)
    except Exception as e:
        await report_error(
            client, e,
            "Ошибка при обработке добавления бота в чат",
            "Произошла ошибка при добавлении в чат",
            message=message, lang=lang)
