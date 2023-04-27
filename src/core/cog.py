"""IMPORTS"""
from discord.ext import commands

from .bot import OtakuBot


"""MAIN CLASS"""


class Cog(commands.Cog):
    def __init__(self, bot: OtakuBot):
        self.bot = bot
        self.config = bot.config
        self.db = bot.db
        self.log = bot.log
        self.current_time = bot.current_time

    async def cog_load(self):
        self.log.info(f"{self.qualified_name} has been loaded")

    async def cog_unload(self):
        self.log.info(f"{self.qualified_name} has been unloaded")
