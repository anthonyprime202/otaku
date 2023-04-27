from .commands import giveaway_group
from .timer import GiveawayTimer
from ...core import OtakuBot


async def setup(bot: OtakuBot):
    await bot.add_cog(GiveawayTimer(bot))
    bot.tree.add_command(giveaway_group)