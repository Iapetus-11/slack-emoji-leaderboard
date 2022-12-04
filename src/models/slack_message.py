from tortoise import fields

from src.models import BaseModel
from src.models.slack_message_emoij_use import SlackMessageEmojiUse


class SlackMessage(BaseModel):
    id = fields.UUIDField(pk=True, unique=True)
    user_id = fields.CharField(max_length=32)
    channel_id = fields.CharField(max_length=32)
    char_count = fields.IntField()
    timestamp = fields.FloatField()

    emojis: fields.ReverseRelation["SlackMessageEmojiUse"]
