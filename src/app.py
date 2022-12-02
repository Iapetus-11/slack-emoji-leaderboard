import asyncio
import logging
from typing import Any

from slack_bolt.async_app import AsyncApp, AsyncSay
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from config import CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = AsyncApp(
    token=CONFIG.SLACK_BOT_TOKEN,
)


@app.event("message")
async def handle_message(message: dict[str, Any], say: AsyncSay):
    logger.info(type(message), message)
    logger.info(type(say), say)


async def on_ready():
    data = await app.client.emoji_list()
    print("#######", data)


async def serve_forever():
    while True:
        await asyncio.sleep(1800)


async def main():
    app_handler = AsyncSocketModeHandler(app, CONFIG.SLACK_APP_TOKEN, logger=logger)
    asyncio.create_task(on_ready())

    await app_handler.connect_async()
    await on_ready()
    await serve_forever()



if __name__ == "__main__":
    asyncio.run(main())

