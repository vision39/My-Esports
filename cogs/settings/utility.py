import discord
from discord.ext import commands
import psutil
import time
# Import the main bot class for type hinting
from core.Bot import ME


class Utility(commands.Cog):
    """General utility commands that are useful for everyone."""

    def __init__(self, bot: ME):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Checks the bot's latency and system status."""

        # 1. Get Discord API Latency
        api_latency = self.bot.latency * 1000  # Convert to milliseconds

        # 2. Measure Database Latency
        db_start_time = time.perf_counter()
        # Execute a simple query to check the connection and measure response time
        await self.bot.db.execute_query("SELECT 1")
        db_end_time = time.perf_counter()
        db_latency = (db_end_time - db_start_time) * 1000

        # 3. Get CPU Utilization
        cpu_usage = psutil.cpu_percent()

        # Create the embed with all the new information
        embed = self.bot.embed(
            title="<a:srt_discordloading:1397925447550898187> Pong!",
            description=(
                f"<a:dot_red:1397925925882036254> API Latency: **{api_latency:.2f}ms**\n"
                f"<a:dot_red:1397925925882036254> Database Latency: **{db_latency:.2f}ms**\n"
                f"<a:dot_red:1397925925882036254> CPU Utilization: **{cpu_usage:.1f}%**"
            )
        )
        await ctx.send(embed=embed)


async def setup(bot: ME):
    """The setup function is required for the bot to load the cog."""
    await bot.add_cog(Utility(bot))
