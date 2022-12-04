import logging
from collections import Counter
from datetime import datetime, timedelta
from typing import Any

import uvicorn
from fastapi import FastAPI, Query
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp
from starlette.middleware import Middleware as StarletteMiddleware
from starlette.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from tortoise.expressions import F
from tortoise.functions import Sum

from src.config import CONFIG, TORTOISE_ORM
from src.models import SlackEmoji, SlackMessage, SlackMessageEmojiUse, SlackUserEmojiReactions
from src.utils.slack import get_block_emojis

logging.basicConfig(level=getattr(logging, CONFIG.LOG_LEVEL))
logger = logging.getLogger("app")

app = AsyncApp(
    token=CONFIG.SLACK_BOT_TOKEN,
)
app_handler = AsyncSocketModeHandler(app, CONFIG.SLACK_APP_TOKEN, logger=logger)

api = FastAPI(
    middleware=[
        StarletteMiddleware(
            CORSMiddleware,
            allow_origins=CONFIG.API_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["*"],
            expose_headers=["*"],
        )
    ],
)


@app.event("message")
async def app_handle_message(event: dict[str, Any]):
    db_message = await SlackMessage.create(
        id=event["client_msg_id"],
        user_id=event["user"],
        channel_id=event["channel"],
        char_count=len(event["text"]),
        timestamp=event["ts"],
    )

    for emoji, count in Counter(get_block_emojis(event.get("blocks", []))).items():
        await SlackMessageEmojiUse.create(message=db_message, emoji_id=emoji, count=count)


@app.event("reaction_added")
async def app_handle_reaction_added(event: dict[str, Any]):
    if event["item"]["type"] != "message":
        return

    user_reactions, _ = await SlackUserEmojiReactions.get_or_create(
        emoji_id=event["reaction"], user_id=event["user"], defaults={"count": 0}
    )

    user_reactions.count += 1
    await user_reactions.save()


@app.event("reaction_removed")
async def app_handle_reaction_removed(event: dict[str, Any]):
    if event["item"]["type"] != "message":
        return

    if user_reactions := await SlackUserEmojiReactions.get_or_none(
        emoji_id=event["reaction"], user_id=event["user"]
    ):
        if user_reactions.count <= 1:
            await user_reactions.delete()
        else:
            user_reactions.count -= 1
            await user_reactions.save()


@api.get("/")
async def api_home():
    return {
        "made_by": {
            "name": "Milo",
            "url": "https://iapetus11.me",
        },
        "source": "https://github.com/Iapetus-11/slack-leaderboard",
    }


@api.get("/emojis/")
async def api_emojis():
    return {emoji.id: emoji.url for emoji in await SlackEmoji.all()}


@api.get("/emojis/leaderboard/")
async def api_emojis_leaderboards(since: datetime = Query(None)):
    if not since:
        since = datetime.utcnow() - timedelta(days=7)

    data = {
        r["emoji_id"]: r["uses"]
        for r in (
            await SlackMessageEmojiUse.filter(created_at__gt=since)
            .group_by("emoji_id")
            .annotate(uses=Sum(F("count")))
            .values("emoji_id", "uses")
        )
    }

    data.update(
        {
            r["emoji_id"]: r["count"]
            for r in await SlackUserEmojiReactions.all().values("emoji_id", "count")
        }
    )

    data = dict(sorted(data.items(), key=(lambda kv: kv[1]), reverse=True))

    return data


async def sync_emojis():
    response = await app.client.emoji_list()

    emojis = dict[str, SlackEmoji]()
    aliases = dict[str, str]()

    for name, url in response.data["emoji"].items():
        # There are emoji "aliases", we handle those later
        if "alias:" in url:
            aliases[name] = url.split(":")[1]
            continue

        emoji_hash = url.split("/")[-1].split(".")[0]

        emojis[name], _ = await SlackEmoji.get_or_create(
            id=name, defaults={"hash": emoji_hash, "url": url}
        )

    # We treat emoji aliases as their own emojis in our db
    for alias_name, name in aliases.items():
        if emoji := emojis.get(name):
            await SlackEmoji.get_or_create(
                id=alias_name, defaults={"hash": emoji.hash, "url": emoji.url}
            )


@api.on_event("startup")
async def api_handle_startup():
    await Tortoise.init(TORTOISE_ORM)

    await app_handler.connect_async()

    await sync_emojis()


@api.on_event("shutdown")
async def api_handle_shutdown():
    await app_handler.close_async()


if __name__ == "__main__":
    uvicorn.run(
        "src.app:api",
        host=CONFIG.API_HOST,
        port=CONFIG.API_PORT,
        log_level=CONFIG.LOG_LEVEL.lower(),
    )
