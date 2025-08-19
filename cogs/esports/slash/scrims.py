import discord
from discord.ext import commands
from datetime import datetime

# Import the main bot class and models
from core.Bot import ME
from models.esports.scrims import Scrim

# Import the view and the IST timezone helper
from ..helper.time_parser import IST


class Scrims(commands.Cog, name="Esports"):
    """Commands for managing scrims."""

    def __init__(self, bot: ME):
        self.bot = bot

    @commands.command(name="smanager", aliases=["sm", "gsm"])
    @commands.has_permissions(manage_guild=True)
    async def scrim_manager(self, ctx: commands.Context):
        """Displays the scrim management dashboard."""
        from ..views.scrims.manager import ScrimManagerView

        scrims = await Scrim.filter(guild_id=ctx.guild.id).order_by("scrim_time")

        # --- CORRECTED FORMATTING LOGIC ---
        if not scrims:
            description = "Click `Create Scrim` button for new scrim."
        else:
            lines = []
            for i, s in enumerate(scrims, 1):
                # Convert the stored UTC time to IST for display
                ist_time = s.scrim_time.astimezone(IST)
                time_str = ist_time.strftime('%I:%M %p IST')
                lines.append(
                    f"{i:02}. <:positive:1397965897498628166> : <#{s.reg_channel_id}> - {time_str}"
                )
            description = "\n".join(lines) + "\n\nClick the `Create Scrim` button to start a new scrim."

        embed = self.bot.embed(
            title="Scrims Manager",
            description=description
        )
        
        embed.set_footer(
            text=f"Total Scrims in this server: {len(scrims)}",
            icon_url=ctx.author.display_avatar.url
        )

        view = ScrimManagerView(self.bot, scrims_exist=bool(scrims))
        
        await ctx.send(embed=embed, view=view)


async def setup(bot: ME):
    """The setup function is required for the bot to load the cog."""
    await bot.add_cog(Scrims(bot))
