from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "slackemoji" DROP COLUMN "hash";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "slackemoji" ADD "hash" VARCHAR(32) NOT NULL;"""
