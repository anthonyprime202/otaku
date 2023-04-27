"""IMPORTS"""
from dotenv import dotenv_values
from discord.ext import commands
import coloredlogs
import discord
import asyncpg
import yaml

from .helpers import Config, DictToObject, get_prefix
from .embed import Embed

from logging.config import dictConfig
from typing import Optional
import logging
import os


"""CONSTANTS"""

INTENTS = discord.Intents.default()
INTENTS.message_content = True


ENV = DictToObject(dotenv_values())

"""MAIN CLASS"""


class OtakuBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            intents=INTENTS,
            status=self.config.presence.status,
            activity=discord.Activity(
                type=self.config.presence.activity, name=self.config.presence.name
            ),
        )

    async def setup_hook(self):
        # Database setup
        self.db: asyncpg.Pool = await asyncpg.create_pool(dsn=ENV.dsn)
        self.log.info("Database connection successful")

        # Extensions setup
        await self.load_extension("jishaku")
        for extension in self.config.extensions:
            await self.load_extension(f"src.extensions.{extension}")

    async def on_ready(self):
        self.log.info(f"Logged in as {self.user}(ID: {self.user.id})")

    def run(self):
        # Logging setup
        os.system("clear" if os.name == "posix" else "cls")
        dictConfig(self.config.logging)
        self.log = logging.getLogger("bot")
        coloredlogs.install(
            logger=self.log,
            fmt=self.config.logging["formatters"]["default"]["format"],
            datefmt=self.config.logging["formatters"]["default"]["datefmt"],
        )
        return super().run(ENV.token, log_handler=None)

    ## Adding and removing server from guilds table
    async def on_guild_join(self, guild: discord.Guild):
        await self.db.execute("INSERT INTO guilds (guild_id), VALUES ($1)", guild.id)
        self.log.info(f"{guild.name} added to guilds table")
    
    async def on_guild_remove(self, guild: discord.Guild):
        await self.db.execute("DELETE FROM guilds WHERE guild_id = $1", guild.id)
        self.log.info(f"{guild.name} removed fron guilds table")


    ## Setting up custom properties
    @property
    def config(self) -> Config:
        with open("config.yaml", mode="r") as file:
            data = yaml.load(file, yaml.FullLoader)
        return Config(data)
    
    def normal_embed(self, message: str, extras: Optional[str] = None) -> Embed:
        return Embed(
            title=message,
            description=extras,
            color=self.config.color.embed
        )
    
    def error_embed(self, error: str, solution: Optional[str] = None) -> Embed:
        return Embed(
            title=error,
            description=solution,
            color=self.config.color.red
        )
