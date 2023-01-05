import asyncio
import logging
from typing import Any

import aiohttp
import discord

from src.config import CONFIG

logging.basicConfig(level=getattr(logging, CONFIG.LOG_LEVEL))
logger = logging.getLogger("bot")

client = discord.Client(intents=discord.Intents(guilds=True, emojis=True))


async def sync_emojis(http: aiohttp.ClientSession):
    guild = client.get_guild(CONFIG.DISCORD_GUILD_ID)
    guild_emoji_names = {e.name for e in guild.emojis}

    slack_emojis: dict[dict[str, Any]] = await (
        await http.get(
            f"{CONFIG.API_ADDRESS}/emojis/", headers={"Authorization": CONFIG.API_AUTH}
        )
    ).json()

    leaderboard: dict[str, int] = await (
        await http.get(
            f"{CONFIG.API_ADDRESS}/emojis/leaderboard/",
            params={"unique": "true", "limit": "50"},
            headers={"Authorization": CONFIG.API_AUTH},
        )
    ).json()

    # Remove emojis not in the leaderboard
    if remove_emoji_coros := [
        guild.delete_emoji(discord_emoji)
        for discord_emoji in guild.emojis
        if discord_emoji.name not in leaderboard
    ]:
        await asyncio.wait(map(asyncio.create_task, remove_emoji_coros))

    async def add_emoji(slack_emoji: str):
        try:
            emoji_image = await (
                await http.get(slack_emojis[slack_emoji]["url"])
            ).read()
            await guild.create_custom_emoji(
                name=slack_emoji.replace("-", "_"),
                image=emoji_image,
            )
        except Exception:
            logger.error(
                f"An exception occurred while syncing emoji {slack_emoji!r}",
                exc_info=True,
            )
            raise

    # Add emojis
    if add_emoji_coros := [
        add_emoji(slack_emoji)
        for slack_emoji in leaderboard.keys()
        if slack_emoji not in guild_emoji_names
    ]:
        await asyncio.wait(map(asyncio.create_task, add_emoji_coros))


async def sync_emojis_task():
    http = aiohttp.ClientSession(headers={"Authorization": CONFIG.API_AUTH})

    while True:
        await client.wait_until_ready()

        try:
            logger.info("Syncing emojis...")
            await sync_emojis(http)
            logger.info("Successfully synced emojis!")
        except Exception:
            logger.error("An error occurred while syncing emojis", exc_info=True)

        await asyncio.sleep(60 * 10)


@client.event
async def on_ready():
    logger.info(f"Connected to Discord ({client.user} {client.user.id})")


async def main():
    async with client:
        asyncio.create_task(sync_emojis_task())
        await client.start(CONFIG.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
