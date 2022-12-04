from tortoise import fields

from src.models import BaseModel


class SlackEmojiAlias(BaseModel):
    id = fields.CharField(pk=True, max_length=64)
    to = fields.ForeignKeyField("models.SlackEmoji", related_name="aliases")
