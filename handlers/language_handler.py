import asyncio

from pyrogram import Client, filters

from loader import app, logger, ADMIN_CHAT_ID
from keyboard.keyboard_buttons import keyboard_start_ru, keyboard_start_gb, keyboard_help
from lang import get_help_text, get_text as _
from utils.get_admins import get_chat_admins
from utils.get_data import get_chat_data


@app.on_callback_query(filters.regex(r"^lang:(ru|en)(_start)?$"))
async def handle_change_lang(client: Client, query):
    """Обработчик смены языка."""
    command_origin = "unknown"
    try:
        lang = query.data.split(":")[1].split("_")[0]
        command_origin = query.data.split("_")[-1]

        if command_origin == "start":
            keyboard = keyboard_start_ru if lang == "ru" else keyboard_start_gb

            await query.message.edit_text(_("start_text", lang), reply_markup=keyboard)
            return await query.answer(_("lang_changed", lang))

        # Получаем конфигурацию чата
        chat_config = await get_chat_data(query.message)
        admins = await get_chat_admins(query.message)

        if query.from_user.id not in admins:
            return await query.answer(_("only_admin_lang", lang))

        if chat_config.language == lang:
            return await query.answer(_("lang_already_set", lang))

        # Меняем язык в памяти, подтверждаем в чате и только потом сохраняем
        chat_config.language = lang
        await query.message.edit_text(get_help_text(chat_config), reply_markup=keyboard_help)
        await asyncio.to_thread(chat_config.save)
        await query.answer(_("lang_changed", lang))
    except Exception as e:
        logger.error(f"Ошибка при обработке смены языка: {e}", exc_info=True)
        await client.send_message(ADMIN_CHAT_ID, f"Произошла ошибка при смене языка {command_origin}: {e}")
