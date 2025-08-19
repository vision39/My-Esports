import discord
import asyncio
from core.Bot import ME
from models.esports.scrims import Scrim
from ...helper.time_parser import parse_time

# --- NEW: A simple view for Yes/No confirmation ---
class ConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60.0)
        self.value = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()


class ScrimEditView(discord.ui.View):
    """An interactive view for editing an existing scrim."""

    def __init__(self, bot: ME, scrim: Scrim):
        super().__init__(timeout=180.0)
        self.bot = bot
        self.scrim = scrim
        
        # --- UPDATED: Pre-populate data from the database ---
        self.data = {
            "Name": "ME Scrims", # Default value as requested
            "Registration Channel": self.bot.get_channel(scrim.reg_channel_id) or "Not-Set",
            "Slotlist Channel": "Not-Set", # Placeholder - field doesn't exist in model yet
            "Success Role": "Not-Set", # Placeholder - field doesn't exist in model yet
            "Mentions": 4, # Placeholder - field doesn't exist in model yet
            "Slots": scrim.total_slots,
            "Open Time": scrim.scrim_time.strftime("%I:%M %p"),
            "Reactions": "✅, ❌", # Placeholder
            "Ping Role": "Not-Set", # Placeholder
            "Open Role": "@everyone", # Placeholder
            "Multi-Register": "Not allowed!", # Placeholder
            "Team Compulsion": "No!", # Placeholder
            "Duplicate Team Name": "Allowed", # Placeholder
            "Autodelete Rejected": "No!", # Placeholder
            "Autodelete Late Messages": "Yes!", # Placeholder
            "Slotlist Start from": 1, # Placeholder
            "Autoclean": "4:00 AM (Channel, Role)", # Placeholder
            "Scrim Days": "Mo, Tu, We, Th, Fr, Sa, Su", # Placeholder
            "Required Lines": "Not set", # Placeholder
            "Duplicate / Fake Tags": ";; Allowed", # Placeholder
        }

    async def build_embed(self) -> discord.Embed:
        """Builds the embed based on the current data."""
        embed = self.bot.embed(
            title="Scrims Editor - Edit Settings",
            description="" # Description is now built from fields
        )
        
        def format_field(key):
            value = self.data.get(key)
            if hasattr(value, 'mention'):
                return value.mention
            else:
                return f"`{value}`"

        # --- NEW EMBED LAYOUT ---
        embed.add_field(name="🇦 Name:", value=format_field('Name'), inline=True)
        embed.add_field(name="🇧 Registration Channel:", value=format_field('Registration Channel'), inline=True)
        embed.add_field(name="🇨 Slotlist Channel:", value=format_field('Slotlist Channel'), inline=True)
        embed.add_field(name="🇩 Success Role:", value=format_field('Success Role'), inline=True)
        embed.add_field(name="🇪 Mentions:", value=format_field('Mentions'), inline=True)
        embed.add_field(name="🇫 Slots:", value=format_field('Slots'), inline=True)
        embed.add_field(name="🇬 Open Time:", value=format_field('Open Time'), inline=True)
        embed.add_field(name="🇭 Reactions:", value=format_field('Reactions'), inline=True)
        embed.add_field(name="🇮 Ping Role:", value=format_field('Ping Role'), inline=True)
        embed.add_field(name="🇯 Open Role:", value=format_field('Open Role'), inline=True)
        embed.add_field(name="🇰 Multi-Register:", value=format_field('Multi-Register'), inline=True)
        embed.add_field(name="🇱 Team Compulsion:", value=format_field('Team Compulsion'), inline=True)
        embed.add_field(name="🇲 Duplicate Team Name:", value=format_field('Duplicate Team Name'), inline=True)
        embed.add_field(name="🇳 Autodelete Rejected:", value=format_field('Autodelete Rejected'), inline=True)
        embed.add_field(name="🇴 Autodelete Late Messages:", value=format_field('Autodelete Late Messages'), inline=True)
        embed.add_field(name="🇵 Slotlist Start from:", value=format_field('Slotlist Start from'), inline=True)
        embed.add_field(name="🇶 Autoclean:", value=format_field('Autoclean'), inline=True)
        embed.add_field(name="🇷 Scrim Days:", value=f"```{self.data['Scrim Days']}```", inline=True)
        embed.add_field(name="🇸 Required Lines:", value=format_field('Required Lines'), inline=True)
        embed.add_field(name="🇹 Duplicate / Fake Tags:", value=format_field('Duplicate / Fake Tags'), inline=True)
        
        embed.set_footer(text="Page - 1/1")
        return embed

    async def placeholder_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("This edit function is not yet implemented.", ephemeral=True)

    # --- BUTTONS (A-T) ---
    @discord.ui.button(label="A", style=discord.ButtonStyle.secondary, row=0)
    async def set_a(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="B", style=discord.ButtonStyle.secondary, row=0)
    async def set_b(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="C", style=discord.ButtonStyle.secondary, row=0)
    async def set_c(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="D", style=discord.ButtonStyle.secondary, row=0)
    async def set_d(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="E", style=discord.ButtonStyle.secondary, row=0)
    async def set_e(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="F", style=discord.ButtonStyle.secondary, row=1)
    async def set_f(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="G", style=discord.ButtonStyle.secondary, row=1)
    async def set_g(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="H", style=discord.ButtonStyle.secondary, row=1)
    async def set_h(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="I", style=discord.ButtonStyle.secondary, row=1)
    async def set_i(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="J", style=discord.ButtonStyle.secondary, row=1)
    async def set_j(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="K", style=discord.ButtonStyle.secondary, row=2)
    async def set_k(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="L", style=discord.ButtonStyle.secondary, row=2)
    async def set_l(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="M", style=discord.ButtonStyle.secondary, row=2)
    async def set_m(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="N", style=discord.ButtonStyle.secondary, row=2)
    async def set_n(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="O", style=discord.ButtonStyle.secondary, row=2)
    async def set_o(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="P", style=discord.ButtonStyle.secondary, row=3)
    async def set_p(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="Q", style=discord.ButtonStyle.secondary, row=3)
    async def set_q(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="R", style=discord.ButtonStyle.secondary, row=3)
    async def set_r(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="S", style=discord.ButtonStyle.secondary, row=3)
    async def set_s(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="T", style=discord.ButtonStyle.secondary, row=3)
    async def set_t(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger, row=4)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Asks for confirmation and deletes the scrim if confirmed."""
        confirm_view = ConfirmView()
        confirm_embed = self.bot.embed(
            title="<a:alert:1397932055555215461> Are you sure?",
            description=f"This will permanently delete the scrim **{self.scrim.title}**.\nThis action cannot be undone."
        )
        
        # Send the confirmation message
        await interaction.response.send_message(embed=confirm_embed, view=confirm_view, ephemeral=True)
        
        # Wait for the user to click "Yes" or "No"
        await confirm_view.wait()
        
        if confirm_view.value is True:
            # If they clicked "Yes", delete the scrim
            await self.scrim.delete()
            await interaction.followup.send("Scrim has been deleted.", ephemeral=True)
            # You might want to return to the main dashboard here as well
        else:
            # If they clicked "No" or the view timed out, just notify them.
            await interaction.followup.send("Deletion cancelled.", ephemeral=True)


    @discord.ui.button(label="Save Changes", style=discord.ButtonStyle.success, row=4)
    async def save_changes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.placeholder_callback(interaction)
