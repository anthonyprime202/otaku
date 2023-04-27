select_giveaway_channel = """
SELECT giveaway_channel
FROM guilds
WHERE guild_id = $1
"""

select_giveaway = """
SELECT * 
FROM giveaways
WHERE completed = FALSE
ORDER BY end_time ASC
"""

select_completed_giveaway = """
SELECT giveaway_id, end_time
WHERE completed = TRUE
"""

insert_giveaway = """
INSERT INTO giveaways (giveaway_id, channel_id, guild_id, host, prize, description, start_time, end_time)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
"""

delete_giveaway = """
DELETE FROM giveaways
WHERE giveaway_id = $1
"""
