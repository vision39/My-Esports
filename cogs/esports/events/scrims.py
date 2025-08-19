from discord.ext import commands, tasks
from core.Bot import ME

class ScrimAutomation(commands.Cog):
    def __init__(self, bot: ME):
        self.bot = bot
        # In the future, we will start a background task here.
        # self.auto_open_scrims.start()

    # @tasks.loop(minutes=1)
    # async def auto_open_scrims(self):
    #     """
    #     This background task will run every minute to check for scrims
    #     that need to have their registration opened or closed automatically.
    #     """
    #     pass

async def setup(bot: ME):
    await bot.add_cog(ScrimAutomation(bot))
