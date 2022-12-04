from tortoise import fields

from src.models import BaseModel


class SlackMessageEmojiUse(BaseModel):
    message = fields.ForeignKeyField("models.SlackMessage")
    emoji = fields.ForeignKeyField("models.SlackEmoji")
    count = fields.IntField()
