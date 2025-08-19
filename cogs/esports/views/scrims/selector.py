import discord
from core.Bot import ME
from models.esports.scrims import Scrim
from .edit import ScrimEditView

class ScrimSelect(discord.ui.Select):
    """A select menu to choose a scrim to edit."""
    # --- UPDATED: Accept the new argument ---
    def __init__(self, bot: ME, scrims: list[Scrim], original_interaction: discord.Interaction):
        self.bot = bot
        self.original_interaction = original_interaction
        options = [
            discord.SelectOption(label=f"ID: {scrim.id} | {scrim.title}", value=str(scrim.id))
            for scrim in scrims
        ]
        super().__init__(placeholder="Select a scrim to edit...", options=options)

    async def callback(self, interaction: discord.Interaction):
        scrim_id = int(self.values[0])
        scrim = await Scrim.get(id=scrim_id)
        
        # Pass the original interaction to the edit view
        edit_view = ScrimEditView(self.bot, scrim, self.original_interaction)
        edit_embed = await edit_view.build_embed()
        
        await interaction.response.edit_message(embed=edit_embed, view=edit_view)

class ScrimSelectorView(discord.ui.View):
    """A view that contains the scrim selection dropdown."""
    # --- UPDATED: Accept the new argument ---
    def __init__(self, bot: ME, scrims: list[Scrim], original_interaction: discord.Interaction):
        super().__init__(timeout=180.0)
        # Pass the argument down to the Select menu
        self.add_item(ScrimSelect(bot, scrims, original_interaction))
