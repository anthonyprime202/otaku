"""IMPORTS"""
from discord import Interaction, NotFound, Member

from ...core import OtakuBot, DictToObject
from .queries import delete_giveaway
from .embeds import GiveawayEndEmbed

from datetime import datetime, timedelta
import random
import re


"""UTILITY FUNCTIONS"""


async def parse_time(inter: Interaction[OtakuBot], start: datetime, duration: str) -> datetime:
    pattern = re.compile("(\d+)\s*(h|s|m|d)+?")
    time_table = {"h": 3600, "s": 1, "m": 60, "d": 86400}
    matches = pattern.findall(duration)

    seconds = 0
    try:
        for value, key in matches:
            seconds += time_table[key] * float(value)

    except KeyError:
        await inter.response.send_message(
            embed=inter.client.error_embed(
                error="Invalid time key used",
                solution="Please use ```\ns: for seconds\nm: for minutes\nh: for hours, \nd: for days\n```",
            ),
            ephemeral=True,
        )
        return False

    except ValueError:
        await inter.response.send_message(
            embed=inter.client.error_embed(
                error=f"Invalid time value", solution=f"{value} is not a number!"
            ),
            ephemeral=True,
        )
        return False

    if seconds < 10:
        await inter.response.send_message(
            embed=inter.client.error_embed(error="Time has to be more than `10 seconds` long"),
            ephemeral=True,
        )
        return False

    end_time = start + timedelta(seconds=seconds)
    return end_time


async def end_giveaway(bot: OtakuBot, giveaway: DictToObject):
    try:
        giveaway_channel = await bot.fetch_channel(giveaway.channel_id)
        giveaway_message = await giveaway_channel.fetch_message(giveaway.giveaway_id)
        host = await giveaway_channel.guild.fetch_member(giveaway.host)
    except NotFound:
        await bot.db.execute(delete_giveaway, giveaway.giveaway_id)
        return

    winner = None
    while not isinstance(winner, Member):
        if giveaway.entries == []:
            await giveaway_message.edit(
                embed=GiveawayEndEmbed(
                    prize=giveaway.prize,
                    host=host.mention,
                    entries=len(giveaway.entries),
                    winner="No entries where availale, therefore no winner appointed",
                    start_time=giveaway.start_time,
                    end_time=giveaway.end_time,
                    description=giveaway.description,
                )
            )
            await bot.db.execute(delete_giveaway, giveaway.giveaway_id)
            return
        try:
            winner_id = random.choice(giveaway.entries)
            winner = await giveaway_channel.guild.fetch_member(winner_id)
        except NotFound:
            giveaway.entries.remove(winner_id)

    await giveaway_message.edit(
        embed=GiveawayEndEmbed(
            prize=giveaway.prize,
            host=host.mention,
            entries=len(giveaway.entries),
            winner=winner.mention,
            start_time=giveaway.start_time,
            end_time=giveaway.end_time,
            description=giveaway.desctiption,
        )
    )
