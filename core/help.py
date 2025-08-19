import discord
from discord.ext import commands
from typing import Optional

class MyHelp(commands.HelpCommand):
    """A custom help command that sends formatted embeds."""

    def __init__(self):
        """Initializes the help command and adds aliases."""
        super().__init__(
            command_attrs={
                "help": "Shows this message about the bot's commands.",
                "aliases": ["h", "cmd", "command"],
            }
        )

    # This method is called when the user types `!help`
    async def send_bot_help(self, mapping):
        bot = self.context.bot
        prefix = self.context.prefix

        # --- UPDATED CODE: Create links string and use it in the description ---
        links_value = ""
        if bot.config.SERVER_LINK and bot.config.BOT_INVITE:
            links_value = (
                f"[Support Server]({bot.config.SERVER_LINK}) | "
                f"[Invite Me]({bot.config.BOT_INVITE})"
            )

        embed = bot.embed(
            title=f"{bot.user.name} Help",
            description=links_value
        )

        # --- Group commands from both cogs under "Settings" ---
        grouped_commands = {}
        for cog, command_list in mapping.items():
            if not cog or cog.qualified_name == "Jishaku":
                continue

            category_name = "Settings" if cog.qualified_name in ["Settings", "Utility"] else cog.qualified_name

            if category_name not in grouped_commands:
                grouped_commands[category_name] = []
            grouped_commands[category_name].extend(command_list)

        for category, commands in grouped_commands.items():
            if filtered_commands := [c.name for c in commands if not c.hidden]:
                commands_str = "`" + "`, `".join(filtered_commands) + "`"
                embed.add_field(name=category, value=commands_str, inline=False)
        
        # The separate links field has been removed.

        # Set the custom footer text
        embed.set_footer(text=f"For more info on a command, use {prefix}help <command>")

        await self.get_destination().send(embed=embed)


    # This method is called when the user types `!help <command>`
    async def send_command_help(self, command: commands.Command):
        bot = self.context.bot
        prefix = self.context.prefix

        embed = bot.embed(
            title=f"Help for: `{command.name}`",
            description=command.help or "No description provided."
        )

        signature = f"`{prefix}{command.qualified_name} {command.signature}`"
        embed.add_field(name="Usage", value=signature, inline=False)

        if command.aliases:
            aliases = "`" + "`, `".join(command.aliases) + "`"
            embed.add_field(name="Aliases", value=aliases, inline=False)

        await self.get_destination().send(embed=embed)

    # This is called for `!help <group>`, which we can treat like a command
    async def send_group_help(self, group: commands.Group):
        await self.send_command_help(group)

    # This is called for `!help <cog>`, but we won't implement it for now
    async def send_cog_help(self, cog: commands.Cog):
        pass
