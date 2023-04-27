import discord
import yaml

from .utils import DictToObject

from datetime import datetime

class Embed(discord.Embed):
    @property
    def colors(self):
        with open("./config.yaml", mode="r") as config:
            data = DictToObject(yaml.load(config, yaml.FullLoader)["color"])
        return data
    
    @property
    def colours(self):
        return self.colors
    
    @property
    def current_time(self) -> datetime:
        """Returns the current utc timestamp"""
        return discord.utils.utcnow()