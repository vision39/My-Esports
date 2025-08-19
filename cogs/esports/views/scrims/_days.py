import discord

# --- NEW: Import the Day enum from your constants file ---
from constants import Day

class DaySelectorView(discord.ui.View):
    """An interactive view for selecting the days a scrim should run."""
    
    def __init__(self, parent_view):
        super().__init__(timeout=180.0)
        self.parent_view = parent_view
        
        # --- UPDATED: Use the Day enum for state management ---
        self.day_states = {day: True for day in Day}
        
        # Create the buttons by iterating through the Day enum
        for i, day in enumerate(Day):
            self.add_item(DayButton(day=day, row=i // 4))

    def build_embed(self) -> discord.Embed:
        """Builds the embed showing the current day selections."""
        description_lines = []
        for day, is_active in self.day_states.items():
            emoji = "<:positive:1397965897498628166>" if is_active else "<:negative3:1397965876917047386>"
            # Use day.name to get the string representation (e.g., "Monday")
            description_lines.append(f"{emoji} {day.name.capitalize()}")
        
        embed = discord.Embed(
            title="Select Scrim Days",
            description="\n".join(description_lines),
            color=self.parent_view.bot.config.COLOR
        )
        return embed

    @discord.ui.button(label="Save", style=discord.ButtonStyle.success, row=3)
    async def save_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Saves the selected days back to the parent wizard view."""
        # --- UPDATED: Generate the abbreviation string from the enum ---
        selected_days = [day.name[:2].capitalize() for day, is_active in self.day_states.items() if is_active]
        
        # Update the parent view's data
        self.parent_view.data["Scrim Days"] = ", ".join(selected_days)
        
        # Re-build the parent embed and show it
        parent_embed = await self.parent_view.build_embed()
        await interaction.response.edit_message(embed=parent_embed, view=self.parent_view)

class DayButton(discord.ui.Button):
    """A button that toggles the state of a specific day."""
    def __init__(self, day: Day, row: int):
        # Use the first two letters of the day's name for the label (e.g., "Mo")
        super().__init__(label=day.name[:2].capitalize(), style=discord.ButtonStyle.secondary, row=row)
        self.day = day

    async def callback(self, interaction: discord.Interaction):
        # Toggle the state in the parent view using the enum member as the key
        self.view.day_states[self.day] = not self.view.day_states[self.day]
        
        # Re-build the embed and update the message
        new_embed = self.view.build_embed()
        await interaction.response.edit_message(embed=new_embed, view=self.view)
