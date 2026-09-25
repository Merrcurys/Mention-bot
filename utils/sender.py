"""Утилиты для определения отправителя сообщения."""


def get_sender_id(message):
    """Возвращает id отправителя сообщения.

    В анонимных сообщениях (от имени группы или канала) поле from_user пустое,
    поэтому используется sender_chat.
    """
    if message.from_user:
        return message.from_user.id

    if message.sender_chat:
        return message.sender_chat.id

    return None


def is_sender_admin(message, admins) -> bool:
    """Проверяет, что сообщение отправил администратор чата.

    Анонимные сообщения от имени группы могут отправлять только администраторы,
    поэтому они также считаются администраторами.
    """
    if message.from_user:
        return message.from_user.id in admins

    if message.sender_chat:
        return message.sender_chat.id == message.chat.id

    return False
