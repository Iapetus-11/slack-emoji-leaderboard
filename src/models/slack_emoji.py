from tortoise import fields
from tortoise.fields import ReverseRelation

from src.models import BaseModel


class SlackEmoji(BaseModel):
    id = fields.CharField(pk=True, max_length=64)
    hash = fields.CharField(max_length=32)
    url = fields.CharField(max_length=128)

    aliases: ReverseRelation["SlackEmojiAlias"]
