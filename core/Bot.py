import asyncio
import os
from datetime import datetime

import discord
from discord.ext import commands
from tortoise import Tortoise, connections

# Import your configuration file
import config as cfg

# Import the Guild model at the top level
from models.misc.guild import Guild
from core.help import MyHelp


# --- Basic Bot Setup ---
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"


# --- The Main Bot Class ---
class ME(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=self.get_prefix,
            intents=intents,
            help_command=MyHelp(),
        )
        self.start_time = datetime.utcnow()

    # --- Properties ---
    @property
    def config(self):
        """A handy shortcut to access the config file."""
        return cfg

    @property
    def db(self):
        """
        A shortcut to the default database connection.
        This property is REQUIRED for the ping command to work.
        """
        return connections.get("default")

    # --- Core Methods ---
    async def setup_hook(self):
        print("Running setup hook...")
        try:
            await Tortoise.init(self.config.TORTOISE)
            await Tortoise.generate_schemas(safe=True)
            print("Successfully connected to the database.")
        except Exception as e:
            print(f"Error connecting to database: {e}")

        print("Loading extensions...")
        for extension in self.config.EXTENSIONS:
            try:
                await self.load_extension(extension)
                print(f"-> Loaded '{extension}'")
            except Exception as e:
                print(f"-> Failed to load '{extension}': {e}")

    async def close(self):
        print("Closing database connections...")
        await Tortoise.close_connections()
        await super().close()

    # --- Helper Methods ---
    async def get_prefix(self, message: discord.Message):
        if not message.guild:
            return commands.when_mentioned_or(self.config.PREFIX)(self, message)

        guild_config = await Guild.get_or_none(id=message.guild.id)
        prefix = guild_config.prefix if guild_config else self.config.PREFIX
        return commands.when_mentioned_or(prefix)(self, message)

    def embed(self, title: str = "", description: str = "") -> discord.Embed:
        return discord.Embed(
            title=title,
            description=description,
            color=self.config.COLOR
        ).set_footer(text=self.config.FOOTER)

    # --- Event Listeners ---
    async def on_ready(self):
        print("-" * 20)
        print(f"Logged in as: {self.user.name} ({self.user.id})")
        print(f"discord.py version: {discord.__version__}")
        print(f"Bot started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print("-" * 20)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        await self.process_commands(message)

        if message.content == f'<@{self.user.id}>':
            # Check if the user has admin-level permissions
            if message.author.guild_permissions.manage_guild:
                # Fetch the prefix for the current guild
                guild_config = await Guild.get_or_none(id=message.guild.id)
                prefix = guild_config.prefix if guild_config else self.config.PREFIX
                # Send the prefix information
                await message.channel.send(f"My prefix in this server is `{prefix}`.")

    async def on_command(self, ctx: commands.Context):
        print(
            f"Command invoked: '{ctx.command.name}' by {ctx.author} ({ctx.author.id}) "
            f"in guild {ctx.guild.name} ({ctx.guild.id})"
        )


# --- Create an instance of the bot ---
bot = ME()
