import inspect

import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.cog import Cog

from ._functions import *


class MyHelpCommand(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    async def send_bot_help(self, mapping):
        ctx = self.context

        cogs = []

        for cog in ctx.bot.cogs.values():
            if await ctx.bot.is_owner(ctx.author):
                cogs.append(cog)
            else:
                cog_commands = [
                    command
                    for command in cog.get_commands()
                    if command.hidden == False and command.enabled == True
                ]
                if len(cog_commands) > 0:
                    cogs.append(cog)

        embed = fancy_embed(
            description=f"Use `{CONFIG['DEFAULT']['PREFIX']}help <Category>` to get help on a category\n\n",
        )

        for cog in cogs:
            if await ctx.bot.is_owner(ctx.author):
                cog_commands = [command for command in cog.get_commands()]
            else:
                if cog._get_overridden_method(cog.cog_check):
                    if inspect.iscoroutinefunction(cog.cog_check):
                        allowed = await cog.cog_check(ctx)
                    else:
                        allowed = cog.cog_check(ctx)
                else:
                    allowed = True

                cog_commands = [
                    command
                    for command in cog.get_commands()
                    if command.hidden == False
                    and command.enabled == True
                    and allowed
                ]

            if len(cog_commands) > 0:
                cog_help = cog.description or "No description provided"
                cog_help += "\n\n"
                cog: Cog
                for command in cog.get_commands():
                    cog_help += f"`{CONFIG['DEFAULT']['PREFIX']}{command.name}`\n{command.short_doc or 'No description provided'}\n\n"  #

                embed.add_field(
                    name=cog.qualified_name, value=cog_help, inline=False
                )

        try:
            embed.set_thumbnail(url=ctx.bot.user.avatar.url)
        except:
            pass

        await ctx.send(embed=embed)

    # Main Help
    async def send_cog_help(self, cog):
        ctx = self.context

        embed = fancy_embed()

        if await ctx.bot.is_owner(ctx.author):
            shown_commands = [command for command in cog.get_commands()]
        else:
            if cog._get_overridden_method(cog.cog_check):
                if inspect.iscoroutinefunction(cog.cog_check):
                    allowed = await cog.cog_check(ctx)
                else:
                    allowed = cog.cog_check(ctx)
            else:
                allowed = True

            shown_commands = [
                command
                for command in cog.get_commands()
                if command.hidden == False and command.enabled == True and allowed
            ]

        if len(shown_commands) == 0:
            return await ctx.send("This cog has no command.")

        if cog.description:
            cog_help = cog.description
        else:
            cog_help = "No description provided for this cog"

        embed.title = f"{cog.qualified_name}"
        embed.description += f"{cog_help}\nUse `{CONFIG['DEFAULT']['PREFIX']}help <command>` to get help on a command.\n\n**Commands :** \n"

        for command in shown_commands:
            embed.description += (
                f"▪︎ {CONFIG['DEFAULT']['PREFIX']}{command.qualified_name} "
            )
            if command.signature:
                embed.description += f"{command.signature} \n"
            else:
                embed.description += "\n"

        try:
            embed.set_thumbnail(url=ctx.bot.user.avatar.url)
        except:
            pass

        await ctx.send(embed=embed)

    # Command Help
    async def send_command_help(self, command):
        ctx = self.context

        embed = fancy_embed()

        if command.cog._get_overridden_method(command.cog.cog_check):
            if inspect.iscoroutinefunction(command.cog.cog_check):
                allowed = await command.cog.cog_check(ctx)
            else:
                allowed = command.cog.cog_check(ctx)
        else:
            allowed = True

        if (
            (command.hidden == True or command.enabled == False) and not allowed
        ) and await ctx.bot.is_owner(ctx.author) == False:
            return await ctx.send(
                f'No command called "{command.qualified_name}" found.'
            )

        if command.signature:
            embed.title = f"{command.qualified_name} {command.signature} \n"
        else:
            embed.title = f"{command.qualified_name}\n"

        embed.description = command.help or "No description provided"

        if len(command.aliases) > 0:
            embed.description += "\nAliases : " + ", ".join(command.aliases)

        try:
            embed.set_thumbnail(url=ctx.bot.user.avatar.url)
        except:
            pass

        await ctx.send(embed=embed)

    # Group Help
    async def send_group_help(self, group):
        ctx = self.context

        embed = fancy_embed()

        if group.signature:
            embed.title = f"{group.qualified_name} {group.signature}"
        else:
            embed.title = group.qualified_name + " - group"

        embed.description = group.help or "No description provided."
        embed.description += f"\nUse `{CONFIG['DEFAULT']['PREFIX']}help {group.qualified_name} <sub_command>` to get help on a group command. \n\n**Subcommands : **\n"

        if await ctx.bot.is_owner(ctx.author):
            group_commands = [command for command in group.commands]
            if len(group_commands) == 0:
                return await ctx.send("This group doesn't have any sub command")
        else:
            if group.cog._get_overridden_method(group.cog.cog_check):
                if inspect.iscoroutinefunction(group.cog.cog_check):
                    allowed = await group.cog.cog_check(ctx)
                else:
                    allowed = group.cog.cog_check(ctx)
            else:
                allowed = True

            group_commands = [
                command
                for command in group.commands
                if command.hidden == False and command.enabled == True and allowed
            ]

        if len(group_commands) == 0:
            return await ctx.send(
                f'No command called "{group.qualified_name}" found.'
            )

        for command in group_commands:
            if command.signature:
                command_help = f"▪︎ {CONFIG['DEFAULT']['PREFIX']}{command.qualified_name} {command.signature} \n"
            else:
                command_help = (
                    f"▪︎ {CONFIG['DEFAULT']['PREFIX']}{command.qualified_name} \n"
                )

            embed.description += command_help

        try:
            embed.set_thumbnail(url=ctx.bot.user.avatar.url)
        except:
            pass
        await ctx.send(embed=embed)

class Help(commands.Cog):
    """Help Command"""

    def __init__(self, bot):
        self.bot = bot
        self.bot._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self.bot._original_help_command


def setup(bot):
    bot.add_cog(Help(bot))
