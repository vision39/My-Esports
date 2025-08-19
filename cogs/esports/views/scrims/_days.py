import discord

class DaySelectorView(discord.ui.View):
    """An interactive view for selecting the days a scrim should run."""
    
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    def __init__(self, parent_view):
        super().__init__(timeout=180.0)
        self.parent_view = parent_view
        
        # Initialize the state of each day (True = active)
        self.day_states = {day: True for day in self.DAYS}
        
        # Create the buttons for each day
        for i, day in enumerate(self.DAYS):
            self.add_item(DayButton(label=day[:2], day_name=day, row=i // 4))

    def build_embed(self) -> discord.Embed:
        """Builds the embed showing the current day selections."""
        description_lines = []
        for day, is_active in self.day_states.items():
            emoji = "<:positive:1397965897498628166>" if is_active else "<:negative3:1397965876917047386>"
            description_lines.append(f"{emoji} {day}")
        
        embed = discord.Embed(
            title="Select Scrim Days",
            description="\n".join(description_lines),
            color=self.parent_view.bot.config.COLOR
        )
        return embed

    @discord.ui.button(label="Save", style=discord.ButtonStyle.success, row=3)
    async def save_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Saves the selected days back to the parent wizard view."""
        selected_days = [day[:2] for day, is_active in self.day_states.items() if is_active]
        
        # Update the parent view's data
        self.parent_view.data["Scrim Days"] = ", ".join(selected_days)
        
        # Re-build the parent embed and show it
        parent_embed = await self.parent_view.build_embed()
        await interaction.response.edit_message(embed=parent_embed, view=self.parent_view)

class DayButton(discord.ui.Button):
    """A button that toggles the state of a specific day."""
    def __init__(self, label: str, day_name: str, row: int):
        super().__init__(label=label, style=discord.ButtonStyle.secondary, row=row)
        self.day_name = day_name

    async def callback(self, interaction: discord.Interaction):
        # Toggle the state in the parent view
        self.view.day_states[self.day_name] = not self.view.day_states[self.day_name]
        
        # Re-build the embed and update the message
        new_embed = self.view.build_embed()
        await interaction.response.edit_message(embed=new_embed, view=self.view)
