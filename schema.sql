CREATE TABLE IF NOT EXISTS guilds (
    guild_id BIGINT PRIMARY KEY,
    prefix VARCHAR(10) DEFAULT '!',
    giveaway_channel BIGINT DEFAULT NULL,
);

CREATE TABLE IF NOT EXISTS giveaways (
    giveaway_id BIGINT PRIMARY KEY,
    channel_id BIGINT NOT NULL,
    guild_id BIGINT NOT NULL,
    host BIGINT NOT NULL,
    prize VARCHAR(128) NOT NULL,
    description VARCHAR(255) DEFAULT '',
    entries BIGINT[] DEFAULT ARRAY[]::BIGINT[],
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    completed BOOLEAN DEFAULT FALSE 
);