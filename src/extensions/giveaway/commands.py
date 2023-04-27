"""IMPORTS"""
from discord import app_commands, Interaction

from .ui import GiveawayModal
from ...core import OtakuBot


"""COMMAND GROUP"""

giveaway_group = app_commands.Group(
    name="giveaway",
    description="Create and manage exciting giveaways",
    guild_only=True
)

@giveaway_group.command(name="create")
async def giveaway_create(inter: Interaction[OtakuBot]):
    await inter.response.send_modal(GiveawayModal())

@giveaway_group.error
async def giveaway_error(inter: Interaction[OtakuBot], error: Exception):
    inter.client.log.error(error)