from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "scrims" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "host_id" BIGINT NOT NULL,
    "title" VARCHAR(200) NOT NULL,
    "scrim_time" TIMESTAMPTZ NOT NULL,
    "scrim_days" VARCHAR(100) NOT NULL DEFAULT 'Mo, Tu, We, Th, Fr, Sa, Su',
    "total_slots" INT NOT NULL DEFAULT 25,
    "is_open" BOOL NOT NULL DEFAULT True,
    "reg_channel_id" BIGINT,
    "reg_message_id" BIGINT,
    "log_channel_id" BIGINT,
    "ping_role_id" BIGINT,
    "registered_teams" JSONB NOT NULL,
    "reserves" JSONB NOT NULL,
    "banned_users" JSONB NOT NULL,
    "open_message" TEXT,
    "dm_message" TEXT
);
COMMENT ON COLUMN "scrims"."reg_channel_id" IS 'The channel where the registration message is posted';
COMMENT ON COLUMN "scrims"."reg_message_id" IS 'The ID of the registration message itself';
COMMENT ON COLUMN "scrims"."log_channel_id" IS 'The channel for sending registration logs';
COMMENT ON COLUMN "scrims"."ping_role_id" IS 'The role to ping when registration opens';
COMMENT ON COLUMN "scrims"."registered_teams" IS 'A list of all registered teams';
COMMENT ON COLUMN "scrims"."reserves" IS 'A list of reserve teams';
COMMENT ON COLUMN "scrims"."banned_users" IS 'A list of users banned from this scrim';
COMMENT ON COLUMN "scrims"."open_message" IS 'Custom message for when registration opens';
COMMENT ON COLUMN "scrims"."dm_message" IS 'Custom DM message on successful registration';
COMMENT ON TABLE "scrims" IS 'Represents a scrim event in the database, with full customization options.';
CREATE TABLE IF NOT EXISTS "guilds" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "prefix" VARCHAR(10) NOT NULL DEFAULT 'm'
);
COMMENT ON TABLE "guilds" IS 'Represents the settings for a guild in the database.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
