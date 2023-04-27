"""IMPORTS"""
from discord.utils import format_dt
import discord

from ...core import Embed

from datetime import datetime
from typing import Optional


"""EMBEDS"""


class GiveawayEmbed(Embed):
    def __init__(
        self,
        prize: str,
        host: str,
        end_time: datetime,
        start_time: datetime,
        description: Optional[str] = None,
        entries: Optional[int] = 0,
    ):
        super().__init__(
            title=prize,
            description=description,
            color=self.colors.fuchsia,
            timestamp=start_time,
        )
        self.set_footer(text="Started")

        hosted_by = f"Hosted by {host}"
        ends_in = f"Ends {format_dt(end_time, style='R')} ({format_dt(end_time, style='f')})"
        entries_str = f"Entries: {entries}"
        self.add_field(
            name="Details", value="\n".join([hosted_by, ends_in, entries_str]), inline=False
        )


class GiveawayEndEmbed(Embed):
    def __init__(
        self,
        prize: str,
        host: str,
        entries: int,
        winner: str,
        start_time: datetime,
        end_time: datetime,
        description: Optional[str] = None,
    ):
        super().__init__(
            title=prize, description=description, color=self.colors.fuchsia, timestamp=start_time
        )
        self.set_footer(text="Started")

        hosted_by = f"Hosted by {host}"
        ended = f"Ended {format_dt(end_time, style='R')} ({format_dt(end_time, style='f')})"
        entries_str = f"Entries: {entries}"
        winner_str = f"Winner: {winner}"
        self.add_field(
            name="Detail", value="\n".join([hosted_by, ended, entries_str, winner_str]), inline=False
        )
