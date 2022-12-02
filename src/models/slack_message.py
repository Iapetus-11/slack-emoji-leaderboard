from tortoise import fields

from src.models import BaseModel


class SlackMessage(BaseModel):
    id = fields.UUIDField(unique=True)
    user_id = fields.CharField(max_length=64)
    timestamp = fields.FloatField()
