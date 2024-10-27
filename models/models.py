import peewee

from models.base import BaseModel


class ChatConfig(BaseModel):
    id = peewee.PrimaryKeyField()
    chat_id = peewee.IntegerField()
    need_access = peewee.BooleanField(default=False)
    is_nickname_visible = peewee.BooleanField(default=True)
    language = peewee.CharField(max_length=3, default='en')

    def __repr__(self) -> str:
        return f"<Chat {self.chat_id}>"

    class Meta:
        table_name = "chat_config"
