import discord
import asyncio
import pytz
from datetime import datetime
from core.Bot import ME
from models.esports.scrims import Scrim
from ...helper.time_parser import parse_time, IST

# --- NEW: Import the manager view to return to it ---

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

    def __init__(self, bot: ME, scrim: Scrim, original_interaction: discord.Interaction):
        super().__init__(timeout=180.0)
        self.bot = bot
        self.scrim = scrim
        self.original_interaction = original_interaction
        
        guild = self.bot.get_guild(scrim.guild_id)
        
        # --- CORRECTED TIME CONVERSION ON LOAD ---
        utc_time = scrim.scrim_time.replace(tzinfo=pytz.utc)
        ist_time = utc_time.astimezone(IST)
        
        self.data = {
            "Name": scrim.title,
            "Registration Channel": self.bot.get_channel(scrim.reg_channel_id) or "Not-Set",
            "Slotlist Channel": self.bot.get_channel(scrim.slotlist_channel_id) or "Not-Set",
            "Success Role": guild.get_role(scrim.success_role_id) if guild else "Not-Set",
            "Mentions": 4, # Placeholder
            "Slots": scrim.total_slots,
            # Format Open Time as only the time string (e.g., '04:00 AM')
            "Open Time": ist_time.strftime("%I:%M %p"),
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
            "Scrim Days": scrim.scrim_days,
            "Required Lines": "Not set", # Placeholder
            "Duplicate / Fake Tags": ";; Allowed", # Placeholder
        }
        self.save_changes.disabled = False

    def _check_save_button_state(self):
        """Checks if all required fields are filled and enables/disables the save button."""
        required_fields = ["Registration Channel", "Slotlist Channel", "Success Role", "Open Time"]
        self.save_changes.disabled = any(self.data[field] == "Not-Set" for field in required_fields)

    async def update_data(self, interaction: discord.Interaction, key: str, value: any):
        """Validates input, updates the scrim data, and refreshes the embed."""
        # --- ADVANCED VALIDATION LOGIC ---
        if key == "Mentions":
            if not str(value).isdigit() or not (0 < int(value) <= 10):
                return await interaction.followup.send("Error: Required mentions must be a number between 1 and 10.", ephemeral=True)
            value = int(value)

        if key == "Slots":
            if not str(value).isdigit() or not (0 < int(value) <= 30):
                return await interaction.followup.send("Error: Total slots must be a number between 1 and 30.", ephemeral=True)
            value = int(value)
        
        if key in ["Registration Channel", "Slotlist Channel"]:
            if not value.startswith("<#"):
                return await interaction.followup.send("Error: Please provide a valid channel mention.", ephemeral=True)
            try:
                channel_id = int("".join(filter(str.isdigit, str(value))))
                channel = await self.bot.fetch_channel(channel_id)
                if not isinstance(channel, discord.TextChannel): raise ValueError()
                value = channel
            except (ValueError, discord.NotFound, discord.Forbidden):
                return await interaction.followup.send("Error: Invalid channel ID or I can't see that channel.", ephemeral=True)

        if key == "Ping Role":
            if value.lower() == "@everyone":
                value = interaction.guild.default_role
            elif not value.startswith("<@&"):
                return await interaction.followup.send("Error: Please provide a valid role mention or '@everyone'.", ephemeral=True)
            else:
                try:
                    role_id = int("".join(filter(str.isdigit, str(value))))
                    role = interaction.guild.get_role(role_id)
                    if not role: raise ValueError()
                    value = role
                except (ValueError, TypeError):
                     return await interaction.followup.send("Error: Invalid role ID.", ephemeral=True)
        
        if key in ["Success Role", "Open Role"]:
            if not value.startswith("<@&"):
                return await interaction.followup.send("Error: Please provide a valid role mention.", ephemeral=True)
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
        
        # Auto-update Slotlist Channel when Reg. Channel is set
        if key == "Registration Channel":
            self.data["Slotlist Channel"] = value

        self._check_save_button_state()
        new_embed = await self.build_embed()
        await interaction.edit_original_response(embed=new_embed, view=self)

    async def build_embed(self) -> discord.Embed:
        """Builds the embed based on the current data."""
        embed = self.bot.embed(
            title="Scrims Editor - Edit Settings",
            description=""
        )
        
        def format_field(key):
            value = self.data.get(key)
            if hasattr(value, 'mention'):
                return value.mention
            else:
                return f"`{value}`"

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
        from .manager import ScrimManagerView
        
        scrims = await Scrim.filter(guild_id=interaction.guild.id).order_by("scrim_time")
        
        if not scrims:
            description = "Click `Create Scrim` button for new scrim."
        else:
            lines = []
            for i, s in enumerate(scrims, 1):
                ist_time = s.scrim_time.astimezone(IST)
                time_str = ist_time.strftime('%I:%M %p IST')
                lines.append(f"{i:02}. <:positive:1397965897498628166> : <#{s.reg_channel_id}> - {time_str}")
            description = "\n".join(lines) + "\n\nClick the `Create Scrim` button to start a new scrim."

        embed = self.bot.embed(title="Scrims Manager", description=description)
        embed.set_footer(text=f"Total Scrims in this server: {len(scrims)}", icon_url=interaction.user.display_avatar.url)
        
        view = ScrimManagerView(self.bot, scrims_exist=bool(scrims))
        await self.original_interaction.edit_original_response(embed=embed, view=view)

    # --- BUTTONS (A-T) ---
    @discord.ui.button(label="A", style=discord.ButtonStyle.secondary, row=0)
    async def set_a(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Name")

    @discord.ui.button(label="B", style=discord.ButtonStyle.secondary, row=0)
    async def set_b(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Registration Channel")

    @discord.ui.button(label="C", style=discord.ButtonStyle.secondary, row=0)
    async def set_c(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Slotlist Channel")

    @discord.ui.button(label="D", style=discord.ButtonStyle.secondary, row=0)
    async def set_d(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Success Role")

    @discord.ui.button(label="E", style=discord.ButtonStyle.secondary, row=0)
    async def set_e(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Mentions")

    @discord.ui.button(label="F", style=discord.ButtonStyle.secondary, row=1)
    async def set_f(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Slots")

    @discord.ui.button(label="G", style=discord.ButtonStyle.secondary, row=1)
    async def set_g(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Open Time")

    @discord.ui.button(label="H", style=discord.ButtonStyle.secondary, row=1)
    async def set_h(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Reactions")

    @discord.ui.button(label="I", style=discord.ButtonStyle.secondary, row=1)
    async def set_i(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Ping Role")

    @discord.ui.button(label="J", style=discord.ButtonStyle.secondary, row=1)
    async def set_j(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Open Role")

    @discord.ui.button(label="K", style=discord.ButtonStyle.secondary, row=2)
    async def set_k(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Multi-Register")

    @discord.ui.button(label="L", style=discord.ButtonStyle.secondary, row=2)
    async def set_l(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Team Compulsion")

    @discord.ui.button(label="M", style=discord.ButtonStyle.secondary, row=2)
    async def set_m(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Duplicate Team Name")

    @discord.ui.button(label="N", style=discord.ButtonStyle.secondary, row=2)
    async def set_n(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Autodelete Rejected")

    @discord.ui.button(label="O", style=discord.ButtonStyle.secondary, row=2)
    async def set_o(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Autodelete Late Messages")

    @discord.ui.button(label="P", style=discord.ButtonStyle.secondary, row=3)
    async def set_p(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Slotlist Start from")

    @discord.ui.button(label="Q", style=discord.ButtonStyle.secondary, row=3)
    async def set_q(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Autoclean")

    @discord.ui.button(label="R", style=discord.ButtonStyle.secondary, row=3)
    async def set_r(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Scrim Days")

    @discord.ui.button(label="S", style=discord.ButtonStyle.secondary, row=3)
    async def set_s(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Required Lines")

    @discord.ui.button(label="T", style=discord.ButtonStyle.secondary, row=3)
    async def set_t(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._get_chat_input(interaction, "Duplicate / Fake Tags")

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger, row=4)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Asks for confirmation and deletes the scrim if confirmed."""
        confirm_view = ConfirmView()
        confirm_embed = self.bot.embed(
            title="⚠️ Are you sure?",
            description=f"This will permanently delete the scrim **{self.scrim.title}**.\nThis action cannot be undone."
        )
        
        await interaction.response.send_message(embed=confirm_embed, view=confirm_view, ephemeral=True)
        await confirm_view.wait()
        
        if confirm_view.value is True:
            await self.scrim.delete()
            await interaction.followup.send("Scrim has been deleted.", ephemeral=True)
            await self._return_to_dashboard(interaction)
        else:
            await interaction.followup.send("Deletion cancelled.", ephemeral=True)

    @discord.ui.button(label="Save Changes", style=discord.ButtonStyle.success, row=4)
    async def save_changes(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Saves the edited data to the database."""
        self.scrim.title = self.data["Name"]
        self.scrim.total_slots = self.data["Slots"]
        self.scrim.scrim_days = self.data["Scrim Days"]
        
        if isinstance(self.data["Registration Channel"], discord.TextChannel):
            self.scrim.reg_channel_id = self.data["Registration Channel"].id
        if isinstance(self.data["Slotlist Channel"], discord.TextChannel):
            self.scrim.slotlist_channel_id = self.data["Slotlist Channel"].id
        if isinstance(self.data["Success Role"], discord.Role):
            self.scrim.success_role_id = self.data["Success Role"].id
        if isinstance(self.data["Ping Role"], discord.Role):
            self.scrim.ping_role_id = self.data["Ping Role"].id
            
        try:
            self.scrim.scrim_time = parse_time(self.data["Open Time"])
        except ValueError as e:
            return await interaction.response.send_message(f"Error in Open Time: {e}", ephemeral=True)

        await self.scrim.save()
        
        await interaction.response.send_message("✅ Changes saved successfully!", ephemeral=True)
        await self._return_to_dashboard(interaction)
