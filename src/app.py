import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from config import CONFIG

app = App(
    token=CONFIG.SLACK_BOT_TOKEN,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.message("test-lb-bot")
def test(message, say):
    print(message)
    say("Hello World!")


if __name__ == "__main__":
    SocketModeHandler(app, CONFIG.SLACK_APP_TOKEN, logger=logger).start()

