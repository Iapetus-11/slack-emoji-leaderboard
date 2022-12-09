from tortoise import fields
from tortoise.fields import ReverseRelation

from src.models import BaseModel


class SlackEmoji(BaseModel):
    id = fields.CharField(pk=True, max_length=64)
    url = fields.CharField(max_length=128)

    aliases: ReverseRelation["SlackEmojiAlias"]  # noqa: F821
