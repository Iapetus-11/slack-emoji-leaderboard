import logging
from collections import Counter, defaultdict
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
from tortoise.functions import Count, Sum
from tortoise.transactions import in_transaction

from src.config import CONFIG, TORTOISE_ORM
from src.docs.route_models import Api_Emojis, Api_Emojis_Leaderboard
from src.models import (
    SlackEmoji,
    SlackEmojiAlias,
    SlackMessage,
    SlackMessageEmojiReaction,
    SlackMessageEmojiUse,
)
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
    # Handle a new message
    if not (event_subtype := event.get('subtype')):
        db_message = await SlackMessage.create(
            id=event["client_msg_id"],
            user_id=event["user"],
            channel_id=event["channel"],
            char_count=len(event["text"]),
            timestamp=event["ts"],
        )

        emoji_counter = Counter(get_block_emojis(event.get("blocks", [])))
        emoji_aliases = {
            a.id: a.to_id for a in await SlackEmojiAlias.filter(id__in=[*emoji_counter.keys()])
        }

        for emoji, count in emoji_counter.items():
            await SlackMessageEmojiUse.create(
                message=db_message, emoji_id=emoji_aliases.get(emoji, emoji), count=count
            )
    # Handle an existing message being edited
    elif event_subtype == "message_changed":
        if message := await SlackMessage.get_or_none(id=event["message"]["client_msg_id"]):
            emoji_counter = Counter(get_block_emojis(event["message"].get("blocks", [])))
            emoji_aliases = {
                a.id: a.to_id for a in await SlackEmojiAlias.filter(id__in=[*emoji_counter.keys()])
            }

            async with in_transaction():
                await SlackMessageEmojiUse.filter(message_id=message.id).delete()

                for emoji, count in emoji_counter.items():
                    await SlackMessageEmojiUse.create(
                        message=message, emoji_id=emoji_aliases.get(emoji, emoji), count=count
                    )
    # Handle an existing message being deleted
    elif event_subtype == "message_deleted":
        if message := await SlackMessage.get_or_none(id=event["previous_message"]["client_msg_id"]):
            await message.delete()


@app.event("reaction_added")
async def app_handle_reaction_added(event: dict[str, Any]):
    if event["item"]["type"] != "message":
        return

    # Using the channel, author, and timestamp we can figure out the actual message that was sent
    # (Because Slack does not send us the message id)
    reaction_message = await SlackMessage.get_or_none(
        channel_id=event["item"]["channel"],
        user_id=event["item_user"],
        timestamp=event["item"]["ts"],
    )

    if reaction_message:
        await SlackMessageEmojiReaction.create(
            emoji_id=event["reaction"],
            user_id=event["user"],
            message=reaction_message,
        )


@app.event("reaction_removed")
async def app_handle_reaction_removed(event: dict[str, Any]):
    if event["item"]["type"] != "message":
        return

    if user_reaction := await SlackMessageEmojiReaction.get_or_none(
        emoji_id=event["reaction"],
        user_id=event["user"],
        message__channel_id=event["item"]["channel"],
        message__user_id=event["item_user"],
        message__timestamp=event["item"]["ts"],
    ):
        await user_reaction.delete()


@api.get("/")
async def api_home():
    return {
        "made_by": {
            "name": "Milo",
            "url": "https://iapetus11.me",
        },
        "source": "https://github.com/Iapetus-11/slack-leaderboard",
        "docs": "/docs",
    }


@api.get(
    "/emojis/",
    description="Fetch a mapping of emojis to their image urls and aliases",
    response_model=Api_Emojis,
)
async def api_emojis():
    return {
        emoji.id: {
            "url": emoji.url,
            "aliases": [a.id for a in emoji.aliases],
        }
        async for emoji in SlackEmoji.all().prefetch_related("aliases")
    }


@api.get(
    "/emojis/leaderboard/",
    description="Fetch a mapping of emojis to their total uses in messages and reactions",
    response_model=Api_Emojis_Leaderboard,
)
async def api_emojis_leaderboards(since: datetime = Query(None)):
    if not since:
        since = datetime.utcnow() - timedelta(days=7)

    message_emoji_use = {
        r["emoji_id"]: r["uses"]
        for r in (
            await SlackMessageEmojiUse.filter(created_at__gt=since)
            .group_by("emoji_id")
            .annotate(uses=Sum(F("count")))
            .values("emoji_id", "uses")
        )
    }

    reaction_emoji_use = {
        r["emoji_id"]: r["uses"]
        for r in (
            await SlackMessageEmojiReaction.filter(created_at__gt=since)
            .group_by("emoji_id")
            .annotate(uses=Count("id"))
            .values("emoji_id", "uses")
        )
    }

    leaderboard = defaultdict[str, int](int)
    for emoji_id, uses in [*message_emoji_use.items(), *reaction_emoji_use.items()]:
        leaderboard[emoji_id] += uses

    return dict(sorted(leaderboard.items(), key=(lambda kv: kv[1]), reverse=True))


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

    for alias_name, name in aliases.items():
        if emoji := emojis.get(name):
            await SlackEmojiAlias.get_or_create(id=alias_name, defaults={"to_id": emoji.id})


@api.on_event("startup")
async def api_handle_startup():
    await Tortoise.init(TORTOISE_ORM)
    logger.info("Initialized Tortoise")

    await app_handler.connect_async()

    await sync_emojis()
    logger.info("Synced Slack emojis to database")


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
