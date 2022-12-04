from tortoise import fields

from src.models import BaseModel


class SlackUserEmojiReactions(BaseModel):
    emoji = fields.ForeignKeyField("models.SlackEmoji")
    user_id = fields.CharField(max_length=32)
    count = fields.IntField()
