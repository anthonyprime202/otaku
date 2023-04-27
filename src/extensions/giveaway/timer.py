"""IMPORTS"""
from discord.ext import tasks
from discord import utils

from .queries import select_giveaway, select_completed_giveaway, delete_giveaway
from .utils import end_giveaway
from ...core import Cog, DictToObject

from datetime import timedelta


"""TIMER CLASS"""


class GiveawayTimer(Cog, name="Giveaway Timer Cog"):
    async def cog_load(self):
        await super().cog_load()
        self.giveaway_timer.start()
        self.reroll_timer.start()

    async def cog_umload(self):
        await super().cog_unload()

    @tasks.loop()
    async def giveaway_timer(self):
        try:
            giveaway = DictToObject(await self.db.fetchrow(select_giveaway))
        except (TypeError, AttributeError):
            self.giveaway_timer.stop()
            return

        if giveaway.end_time >= self.current_time():
            await utils.sleep_until(giveaway.end_time)
        await end_giveaway(self.bot, giveaway)

    @giveaway_timer.before_loop
    async def before_giveaway_timer(self):
        await self.bot.wait_until_ready()
    
    @giveaway_timer.error
    async def giveaway_timer_error(self, error: Exception):
        self.log.error(error)

    @tasks.loop(hours=24)
    async def reroll_timer(self):
        try:
            data = await self.db.fetch(select_completed_giveaway)
        except TypeError:
            return
        
        parsed = [(record["giveaway_id"], (record["end_time"] + timedelta(days=1))) for record in data]
        deletion = []
        for item in parsed:
            if item[1] < self.current_time():
                deletion.append([item[0]])

        await self.db.executemany(delete_giveaway, deletion)
    
    @reroll_timer.before_loop
    async def before_reroll_timer(self):
        await self.bot.wait_until_ready()

    @reroll_timer.error
    async def reroll_timer_error(self, error: Exception):
        self.log.error(error)

