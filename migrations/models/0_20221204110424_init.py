from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "slackemoji" (
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" VARCHAR(64) NOT NULL  PRIMARY KEY,
    "hash" VARCHAR(32) NOT NULL,
    "url" VARCHAR(128) NOT NULL
);
CREATE TABLE IF NOT EXISTS "slackmessage" (
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "user_id" VARCHAR(32) NOT NULL,
    "channel_id" VARCHAR(32) NOT NULL,
    "char_count" INT NOT NULL,
    "timestamp" DOUBLE PRECISION NOT NULL
);
CREATE TABLE IF NOT EXISTS "slackmessageemojireaction" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" VARCHAR(32) NOT NULL,
    "emoji_id" VARCHAR(64) NOT NULL REFERENCES "slackemoji" ("id") ON DELETE CASCADE,
    "message_id" UUID NOT NULL REFERENCES "slackmessage" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "slackmessageemojiuse" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "count" INT NOT NULL,
    "emoji_id" VARCHAR(64) NOT NULL REFERENCES "slackemoji" ("id") ON DELETE CASCADE,
    "message_id" UUID NOT NULL REFERENCES "slackmessage" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
