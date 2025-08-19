import discord
from core.Bot import ME
from models.esports.scrims import Scrim
from .edit import ScrimEditView

class ScrimSelect(discord.ui.Select):
    """A select menu to choose a scrim to edit."""
    def __init__(self, bot: ME, scrims: list[Scrim]):
        self.bot = bot
        options = [
            discord.SelectOption(label=f"ID: {scrim.id} | {scrim.title}", value=str(scrim.id))
            for scrim in scrims
        ]
        super().__init__(placeholder="Select a scrim to edit...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Get the ID of the scrim the user selected
        scrim_id = int(self.values[0])
        
        # Fetch the full scrim object from the database
        scrim = await Scrim.get(id=scrim_id)
        
        # Create and show the editor view for the selected scrim
        edit_view = ScrimEditView(self.bot, scrim)
        edit_embed = await edit_view.build_embed()
        await interaction.response.edit_message(embed=edit_embed, view=edit_view)

class ScrimSelectorView(discord.ui.View):
    """A view that contains the scrim selection dropdown."""
    def __init__(self, bot: ME, scrims: list[Scrim]):
        super().__init__(timeout=180.0)
        self.add_item(ScrimSelect(bot, scrims))
