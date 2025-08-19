import discord
from discord.ext import commands

# Import the main bot class for type hinting
from core.Bot import ME

# Import the database model we created
from models.misc.guild import Guild


class Settings(commands.Cog):
    """Commands for managing server-specific settings."""

    def __init__(self, bot: ME):
        self.bot = bot

    @commands.command(name="setprefix")
    @commands.has_permissions(manage_guild=True)
    async def set_prefix(self, ctx: commands.Context, new_prefix: str):
        """Sets a custom command prefix for this server."""

        if len(new_prefix) > 10:
            return await ctx.send("The prefix can't be longer than 10 characters.")

        await Guild.update_or_create(defaults={"prefix": new_prefix}, id=ctx.guild.id)

        embed = self.bot.embed(
            title="✅ Prefix Updated",
            description=f"My prefix in this server has been changed to `{new_prefix}`.",
        )
        await ctx.send(embed=embed)


async def setup(bot: ME):
    """The setup function is required for the bot to load the cog."""
    await bot.add_cog(Settings(bot))
