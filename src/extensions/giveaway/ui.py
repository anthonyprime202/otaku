"""IMPORTS"""
from discord import ui, Interaction
from discord.ext.tasks import Loop
import discord

from .queries import select_giveaway_channel, insert_giveaway
from .embeds import GiveawayEmbed
from .utils import parse_time
from ...core import OtakuBot


"""VIEWS"""


"""MODALS"""


class GiveawayModal(ui.Modal):
    duration = ui.TextInput(
        label="Duration",
        placeholder="e.g. 25d 2h 5m 30s",
        custom_id="giveaway:setup:modal:duration:textinput",
    )
    prize = ui.TextInput(
        label="Prize",
        placeholder="what's the winner gonna get?",
        max_length=128,
        custom_id="giveaway:setup:moadal:prize:textinput",
    )
    description = ui.TextInput(
        label="Description",
        style=discord.TextStyle.long,
        placeholder="wanna describe the giveaway?",
        max_length=255,
        required=False,
        custom_id="giveaway:setup:moadal:description:textinput",
    )

    def __init__(self):
        super().__init__(
            title="Create Giveaway!",
            timeout=None,
            custom_id="giveaway:setup:modal",
        )

    async def on_submit(self, inter: Interaction[OtakuBot]):
        # Parsing time
        start_time = inter.client.current_time()
        end_time = await parse_time(inter, start_time, self.duration.value)
        if end_time is False:
            return

        # Getting giveaway channel
        giveaway_channel_id = await inter.client.db.fetchval(
            select_giveaway_channel, inter.guild_id
        )
        giveaway_channel = (
            inter.channel
            if giveaway_channel_id is None
            else (await inter.guild.fetch_channel(giveaway_channel_id))
        )

        # Sending the giveaway message
        giveaway_message: discord.Message = await giveaway_channel.send(
            embed=GiveawayEmbed(
                prize=self.prize.value,
                host=inter.user.mention,
                end_time=end_time,
                start_time=start_time,
                description=self.description.value,
            )
        )

        # Updating the giveaway to database
        await inter.client.db.execute(
            insert_giveaway,
            giveaway_message.id,
            giveaway_channel.id,
            inter.guild_id,
            inter.user.id,
            self.prize.value,
            self.description.value,
            start_time,
            end_time,
        )

        # Adding a short response
        await inter.response.send_message(
            embed=inter.client.normal_embed(
                message=f"Giveaway Started! (ID: {giveaway_message.id})",
                extras="Tip: use `setup channel giveaway` to setup a giveaway channel"
                if giveaway_channel_id is None
                else None,
            ),
            ephemeral=True,
        )

        # Restarting timer
        giveaway_timer = inter.client.cogs["Giveaway Timer Cog"].giveaway_timer
        if giveaway_timer.is_running():
            giveaway_timer.restart()
        else:
            giveaway_timer.start()

    async def on_error(self, inter: Interaction[OtakuBot], error: Exception):
        inter.client.log.error(error)
