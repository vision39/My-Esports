import discord
import asyncio
import pytz
from core.Bot import ME
from models.esports.scrims import Scrim
from ...helper.time_parser import parse_time, IST
from ._days import DaySelectorView

class ScrimWizardView(discord.ui.View):
    """An interactive view for creating a new scrim step-by-step using chat input."""

    def __init__(self, bot: ME, original_interaction: discord.Interaction):
        super().__init__(timeout=180.0)
        self.bot = bot
        self.original_interaction = original_interaction
        
        self.data = {
            "Reg. Channel": "Not-Set",
            "Slotlist Channel": "Not-Set",
            "Success Role": "Not-Set",
            "Req. Mentions": 4,
            "Total Slots": 25,
            "Open Time": "Not-Set",
            "Scrim Days": "Mo, Tu, We, Th, Fr, Sa, Su",
            "Reactions": "✅, ❌",
        }
        self.save_scrim.disabled = True

    def _check_save_button_state(self):
        """Checks if all required fields are filled and enables/disables the save button."""
        required_fields = ["Reg. Channel", "Success Role", "Open Time"]
        self.save_scrim.disabled = any(self.data[field] == "Not-Set" for field in required_fields)

    async def update_data(self, interaction: discord.Interaction, key: str, value: any):
        """Validates input, updates the scrim data, and refreshes the embed."""
        if key == "Req. Mentions":
            if not str(value).isdigit() or not (0 < int(value) <= 10):
                return await interaction.followup.send("Error: Required mentions must be a number between 1 and 10.", ephemeral=True)
            value = int(value)

        if key == "Total Slots":
            if not str(value).isdigit() or not (0 < int(value) <= 30):
                return await interaction.followup.send("Error: Total slots must be a number between 1 and 30.", ephemeral=True)
            value = int(value)
        
        if key in ["Reg. Channel", "Slotlist Channel"]:
            if not value.startswith("<#") and not value.isdigit():
                return await interaction.followup.send("Error: Please provide a valid channel mention or ID.", ephemeral=True)
            try:
                channel_id = int("".join(filter(str.isdigit, str(value))))
                channel = await self.bot.fetch_channel(channel_id)
                if not isinstance(channel, discord.TextChannel): raise ValueError()
                value = channel
            except (ValueError, discord.NotFound, discord.Forbidden):
                return await interaction.followup.send("Error: Invalid channel ID or I can't see that channel.", ephemeral=True)

        if key == "Success Role":
            if not value.startswith("<@&") and not value.isdigit():
                return await interaction.followup.send("Error: Please provide a valid role mention or ID.", ephemeral=True)
            try:
                role_id = int("".join(filter(str.isdigit, str(value))))
                role = interaction.guild.get_role(role_id)
                if not role: raise ValueError()
                value = role
            except (ValueError, TypeError):
                 return await interaction.followup.send("Error: Invalid role ID.", ephemeral=True)
        
        if key == "Open Time":
            try:
                parse_time(value)
            except ValueError as e:
                return await interaction.followup.send(f"Error: {e}", ephemeral=True)

        self.data[key] = value
        
        if key == "Reg. Channel" and self.data["Slotlist Channel"] == "Not-Set":
            self.data["Slotlist Channel"] = value

        self._check_save_button_state()
        new_embed = await self.build_embed()
        await interaction.edit_original_response(embed=new_embed, view=self)

    async def build_embed(self) -> discord.Embed:
        """Builds the embed based on the current data."""
        embed = self.bot.embed(
            title="Enter details & Press Save",
            description="Scrim Creation is a piece of cake through the dashboard."
        )
        
        def format_field(key):
            value = self.data.get(key)
            return value.mention if hasattr(value, 'mention') else f"`{value}`"

        embed.add_field(name="🇦 Reg. Channel:", value=format_field('Reg. Channel'), inline=True)
        embed.add_field(name="🇧 Slotlist Channel:", value=format_field('Slotlist Channel'), inline=True)
        embed.add_field(name="🇨 Success Role:", value=format_field('Success Role'), inline=True)
        embed.add_field(name="🇩 Req. Mentions:", value=format_field('Req. Mentions'), inline=True)
        embed.add_field(name="🇪 Total Slots:", value=format_field('Total Slots'), inline=True)
        embed.add_field(name="🇫 Open Time:", value=format_field('Open Time'), inline=True)
        embed.add_field(name="🇬 Scrim Days:", value=f"```{self.data['Scrim Days']}```", inline=False)
        embed.add_field(name="🇭 Reactions:", value=self.data['Reactions'], inline=False)
        embed.set_footer(text="EliteQ Premium servers can set custom reactions.")
        return embed

    async def _get_chat_input(self, interaction: discord.Interaction, key: str):
        """Helper function to wait for and process chat input."""
        prompt_embed = discord.Embed(
            description=f"Please send the new value for **{key}** in the chat.",
            color=self.bot.config.COLOR
        )
        prompt = await interaction.channel.send(embed=prompt_embed)
        await interaction.response.defer()

        try:
            message = await self.bot.wait_for("message", timeout=60.0, check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
        except asyncio.TimeoutError:
            await prompt.delete()
            return await interaction.followup.send("You took too long to respond.", ephemeral=True)

        await prompt.delete()
        try: await message.delete()
        except discord.NotFound: pass

        await self.update_data(interaction, key, message.content)

    async def _return_to_dashboard(self, interaction: discord.Interaction):
        """A helper function to build and send the main scrim manager dashboard."""
        from ..scrims.manager import ScrimManagerView
        scrims = await Scrim.filter(guild_id=interaction.guild.id).order_by("scrim_time")
        
        if not scrims:
            description = "Click `Create Scrim` button for new scrim."
        else:
            lines = []
            for i, s in enumerate(scrims, 1):
                # --- CORRECTED TIME CONVERSION ---
                utc_time = s.scrim_time.replace(tzinfo=pytz.utc)
                ist_time = utc_time.astimezone(IST)
                time_str = ist_time.strftime('%I:%M %p IST')
                lines.append(
                    f"{i:02}. <:positive:1397965897498628166> : <#{s.reg_channel_id}> - {time_str}"
                )
            description = "\n".join(lines) + "\n\nClick the `Create Scrim` button to start a new scrim."

        embed = self.bot.embed(title="Scrims Manager", description=description)
        embed.set_footer(text=f"Total Scrims in this server: {len(scrims)}", icon_url=interaction.user.display_avatar.url)
        
        view = ScrimManagerView(self.bot, scrims_exist=bool(scrims))
        if interaction.response.is_done():
            await self.original_interaction.edit_original_response(embed=embed, view=view)
        else:
            await interaction.response.edit_message(embed=embed, view=view)

    # --- BUTTONS ---
    @discord.ui.button(label="A", style=discord.ButtonStyle.secondary, row=1)
    async def set_reg_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Reg. Channel")

    @discord.ui.button(label="B", style=discord.ButtonStyle.secondary, row=1)
    async def set_slotlist_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Slotlist Channel")

    @discord.ui.button(label="C", style=discord.ButtonStyle.secondary, row=1)
    async def set_success_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Success Role")

    @discord.ui.button(label="D", style=discord.ButtonStyle.secondary, row=1)
    async def set_mentions(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Req. Mentions")

    @discord.ui.button(label="E", style=discord.ButtonStyle.secondary, row=1)
    async def set_slots(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Total Slots")
        
    @discord.ui.button(label="F", style=discord.ButtonStyle.secondary, row=2)
    async def set_open_time(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Open Time")

    @discord.ui.button(label="G", style=discord.ButtonStyle.secondary, row=2)
    async def set_scrim_days(self, interaction: discord.Interaction, button: discord.ui.Button):
        day_view = DaySelectorView(parent_view=self)
        day_embed = day_view.build_embed()
        await interaction.response.edit_message(embed=day_embed, view=day_view)

    @discord.ui.button(label="H", style=discord.ButtonStyle.secondary, row=2)
    async def set_reactions(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Reactions")

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger, row=3)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Returns to the main scrim manager dashboard."""
        await self._return_to_dashboard(interaction)

    @discord.ui.button(label="Save Scrim", style=discord.ButtonStyle.success, row=3)
    async def save_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Validates and saves the scrim to the database."""
        scrim_time = parse_time(self.data["Open Time"])
        title = f"Scrim @ {scrim_time.strftime('%I:%M %p')}"

        await Scrim.create(
            guild_id=interaction.guild.id,
            host_id=interaction.user.id,
            title=title,
            scrim_time=scrim_time,
            total_slots=self.data["Total Slots"],
            reg_channel_id=self.data["Reg. Channel"].id,
            slotlist_channel_id=self.data["Slotlist Channel"].id if isinstance(self.data["Slotlist Channel"], discord.TextChannel) else None,
            success_role_id=self.data["Success Role"].id if isinstance(self.data["Success Role"], discord.Role) else None,
            scrim_days=self.data["Scrim Days"]
        )
        
        await interaction.response.send_message("✅ Scrim saved successfully!", ephemeral=True)
        await self._return_to_dashboard(interaction)
