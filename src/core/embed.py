import discord
import yaml

from .helpers import DictToObject

class Embed(discord.Embed):
    @property
    def colors(self):
        with open("./config.yml", mode="r") as config:
            data = DictToObject(yaml.load(config, yaml.FullLoader)["color"])
        return data
    
    @property
    def colours(self):
        return self.colors