from pyrogram import Client, filters
from pyrogram.types import Message

from loader import app, logger, ADMIN_CHAT_ID
from keyboard.keyboard_buttons import keyboard_help
from lang import get_text as _
from utils.get_data import get_chat_data


@app.on_message(filters.new_chat_members)
async def adding_bot_group(client: Client, message: Message):
    """Выводит меню команд при добавлении бота в группу."""
    try:
        if message.new_chat_members and message.new_chat_members[0].is_self:
            chat_id = message.chat.id

            # Получаем конфигурацию чата
            chat_config = await get_chat_data(message)
            lang = chat_config.language

            await client.send_message(chat_id, _("help_text", lang),
                                      reply_markup=keyboard_help, disable_web_page_preview=True)
    except Exception as e:
        logger.error(f"Ошибка при обработке добавления бота в чат: {e}", exc_info=True)
        await client.send_message(ADMIN_CHAT_ID, f"Произошла ошибка при добавлении в чат.")