"""IMPORTS"""
from discord.ext import tasks
from discord import utils

from .queries import select_giveaway
from .utils import end_giveaway
from ...core import Cog, DictToObject


"""TIMER CLASS"""


class GiveawayTimer(Cog, name="Giveaway Timer Cog"):
    async def cog_load(self):
        await super().cog_load()

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
    
    # @giveaway_timer.error
    # async def giveaway_timer_error(self, error: Exception):
    #     self.log.error(error)