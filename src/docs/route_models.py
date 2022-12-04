from pydantic import BaseModel


class Api_Emojis(BaseModel):
    class Api_Emojis_Value(BaseModel):
        url: str
        aliases: list[str]

    __root__: dict[str, Api_Emojis_Value]

    class Config:
        schema_extra = {
            "example": {
                "evil-milo": {
                    "url": "https://emoji.slack-edge.com/T0E2GB46A/evil-milo/a2da0a3ce6da9618.png",
                    "aliases": [],
                },
                "koda-pet": {
                    "url": "https://emoji.slack-edge.com/T0E2GB46A/koda-pet/3afe40f46dbb0df2.gif",
                    "aliases": [],
                },
                "smug": {
                    "url": "https://emoji.slack-edge.com/T0E2GB46A/smug/d88c2a0597ef61d5.png",
                    "aliases": ["evil"],
                },
            }
        }


class Api_Emojis_Leaderboard(BaseModel):
    __root__: dict[str, int]

    class Config:
        schema_extra = {
            "example": {
                "evil-milo": 16,
                "koda-pet": 4,
                "smug": 1,
            }
        }
