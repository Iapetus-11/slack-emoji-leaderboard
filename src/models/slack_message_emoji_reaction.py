from tortoise import fields

from src.models import BaseModel


class SlackMessageEmojiReaction(BaseModel):
    message = fields.ForeignKeyField("models.SlackMessage", related_name="reactions")
    emoji = fields.ForeignKeyField("models.SlackEmoji", related_name="reaction_uses")
    user_id = fields.CharField(max_length=32)
