from tortoise import fields

from src.models import BaseModel


class SlackMessageEmojiUse(BaseModel):
    message = fields.ForeignKeyField("models.SlackMessage", related_name="emojis")
    emoji = fields.ForeignKeyField("models.SlackEmoji", related_name="message_uses")
    count = fields.IntField()
