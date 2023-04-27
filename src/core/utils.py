"""IMPORTS"""
from discord.ext import commands
import discord

from typing import Optional

class DictToObject():
    def __init__(self, attributes: dict[str]):
        for key, value in attributes.items():
            setattr(self, key.lower(), value)


"""Config Class"""

class Config(DictToObject):
    def __init__(self, attributes: dict):
        super().__init__(attributes)
        self.color = ColorConfig(attributes["color"])
        self.presence = PresnceConfig(attributes["presence"])
    

class PresnceConfig():
    def __init__(self, attributes: dict):
        self.attributes = attributes
        self.name = attributes["name"]
    
    @property
    def status(self) -> Optional[discord.Status]:
        match self.attributes["status"]:
            case "idle":
                return discord.Status.idle
            case "dnd": 
                return discord.Status.dnd 
            case "offline": 
                return discord.Status.offline
            case "online":
                return discord.Status.online
            case _:
                return None
    
    @property
    def activity(self) -> Optional[discord.ActivityType]:
        match self.attributes["activity"]:
            case "watching":
                return discord.ActivityType.watching
            case "competing":
                return discord.ActivityType.competing
            case "playing":
                return discord.ActivityType.playing
            case "listening":        
                return discord.ActivityType.listening
            case _:
                return None

class ColorConfig(DictToObject):
    def __init__(self, attributes: dict):
        super().__init__(attributes)


"""Get Prefix Function"""

async def get_prefix(bot, message: discord.Message):
    try:
        prefix = await bot.db.fetchval("SELECT prefix FROM guilds WHERE guild_id = $1", message.guild.id)
    except Exception as e:
        bot.log.error(e)
    return commands.when_mentioned_or(prefix)(bot, message)
