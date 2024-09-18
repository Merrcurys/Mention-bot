from models.models import ChatConfig


def create_table_if_not_exists(chat_id: int):
    if not ChatConfig.select().where(ChatConfig.chat_id == chat_id).exists():
        ChatConfig.create(chat_id=chat_id)