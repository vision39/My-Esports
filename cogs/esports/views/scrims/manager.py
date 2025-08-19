import discord
import asyncio
from core.Bot import ME
from models.esports.scrims import Scrim

# Import the views for the wizard, editor, and our new selector
from ._wiz import ScrimWizardView
from .edit import ScrimEditView
from .selector import ScrimSelectorView

class ScrimManagerView(discord.ui.View):
    """A view containing all the buttons for the scrim manager dashboard."""

    def __init__(self, bot: ME, scrims_exist: bool):
        super().__init__(timeout=None)
        self.bot = bot

        if not scrims_exist:
            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.label != "Create Scrim":
                    item.disabled = True

    async def placeholder_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("This feature is not yet implemented.", ephemeral=True)

    @discord.ui.button(label="Create Scrim", style=discord.ButtonStyle.success, row=0)
    async def create_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):
        wizard_view = ScrimWizardView(self.bot, interaction)
        wizard_embed = await wizard_view.build_embed()
        await interaction.response.edit_message(embed=wizard_embed, view=wizard_view)

    @discord.ui.button(label="Edit Settings", style=discord.ButtonStyle.primary, row=0)
    async def edit_settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Displays a dropdown to select a scrim to edit."""
        # 1. Fetch all scrims for the server
        scrims = await Scrim.filter(guild_id=interaction.guild.id).order_by("scrim_time")
        
        # This button is disabled if no scrims exist, so we don't need an extra check here.

        # 2. Create the selector view and a prompt embed
        selector_view = ScrimSelectorView(self.bot, scrims)
        prompt_embed = self.bot.embed(description="Please select a scrim to edit from the dropdown below.")
        
        # 3. Edit the message to show the dropdown
        await interaction.response.edit_message(embed=prompt_embed, view=selector_view)


    @discord.ui.button(label="Instant Start/Stop Reg", style=discord.ButtonStyle.danger, row=0)
    async def toggle_reg(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="Reserve Slots", style=discord.ButtonStyle.success, row=0)
    async def reserve_slots(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)
        
    @discord.ui.button(label="Ban/Unban", style=discord.ButtonStyle.danger, row=0)
    async def ban_unban(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="Design", style=discord.ButtonStyle.primary, row=1)
    async def design(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="Manage Slotlist", style=discord.ButtonStyle.success, row=1)
    async def manage_slotlist(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="Enable/Disable", style=discord.ButtonStyle.danger, row=1)
    async def enable_disable(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)
        
    @discord.ui.button(label="Need Help!", style=discord.ButtonStyle.danger, row=1)
    async def need_help(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)
        
    @discord.ui.button(label="Drop Location Panel", style=discord.ButtonStyle.primary, row=1)
    async def drop_location(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)
