import logging
import traceback

import aiohttp
import nextcord
from nextcord import Webhook
from nextcord.ext import commands

from ._functions import *


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if hasattr(ctx.command, "on_error"):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.errors.CommandNotFound,)
        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.errors.DisabledCommand):
            await ctx.reply(f"{ctx.command} has been disabled.")

        elif isinstance(error, commands.errors.NoPrivateMessage):
            try:
                await ctx.author.send(
                    f"{ctx.command} can not be used in Private Messages."
                )
            except nextcord.HTTPException:
                pass

        elif isinstance(error, commands.errors.BadArgument):
            await ctx.reply(
                f"Bad Argument. To see the correct syntax use: `{CONFIG['DEFAULT']['PREFIX']}help {ctx.command.name}`"
            )

        elif isinstance(error, commands.errors.TooManyArguments):
            await ctx.reply(
                f"Bad Argument. To see the correct syntax use: `{CONFIG['DEFAULT']['PREFIX']}help {ctx.command.name}`"
            )

        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(
                f"Missing Argument. To see the correct syntax use: `{CONFIG['DEFAULT']['PREFIX']}help {ctx.command.name}`"
            )

        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply(f"You dont have permissions for this Command.")

        elif isinstance(error, commands.errors.NotOwner):
            await ctx.reply(f"You are not the Owner of this bot.")

        elif isinstance(error, commands.errors.BotMissingPermissions):
            await ctx.reply(
                f"Im missing following permission: `{', '.join([x for x in error.missing_perms])}`"
            )

        elif isinstance(error, commands.errors.CheckFailure):
            await ctx.reply(f"You dont have permissions for this Command.")

        else:
            logging.error("Ignoring exception in command {}:".format(ctx.command))
            logging.error(
                traceback.format_exception(type(error), error, error.__traceback__)
            )

            if CONFIG["DEFAULT"]["ERROR_WEBHOOK_URL"] != "":
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(
                        CONFIG["DEFAULT"]["ERROR_WEBHOOK_URL"], session=session
                    )

                    text = "".join(
                        traceback.format_exception(
                            type(error), error, error.__traceback__
                        )
                    )
                    text = (
                        f"**Ignoring exception in command `{ctx.command}`\n**"
                        + "```"
                        + text
                        + "```"
                    )
                    await webhook.send(text)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
