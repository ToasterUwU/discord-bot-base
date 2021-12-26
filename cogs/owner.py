import nextcord
from nextcord.ext import commands

from ._functions import *


class Owner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)

    @commands.command(name="play", hidden=True)
    async def play_status(self, ctx: commands.Context, *, status: str):
        """
        Sets a 'playing' Status
        """
        await self.bot.change_presence(activity=nextcord.Game(status))
        await ctx.message.add_reaction("✅")

    @commands.command(name="watch", hidden=True)
    async def watch_status(self, ctx: commands.Context, *, status: str):
        """
        Sets a 'watching' Status
        """
        await self.bot.change_presence(
            activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=status)
        )
        await ctx.message.add_reaction("✅")

    @commands.command(name="listen", hidden=True)
    async def listen_status(self, ctx: commands.Context, *, status: str):
        """
        Sets a 'listening' Status
        """
        await self.bot.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.listening, name=status
            )
        )
        await ctx.message.add_reaction("✅")

    # Hidden means it won't show up on the default help.
    @commands.command(name="load", hidden=True)
    async def load_cog(self, ctx, *, cog: str):
        """Loads a Module."""

        try:
            self.bot.load_extension("cogs." + cog)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.message.add_reaction("✅")

    @commands.command(name="unload", hidden=True)
    async def unload_cog(self, ctx, *, cog: str):
        """Unloads a Module."""

        try:
            self.bot.unload_extension("cogs." + cog)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.message.add_reaction("✅")

    @commands.command(name="reload", hidden=True)
    async def reload_cog(self, ctx, *, cog: str):
        """Reloads a Module."""

        try:
            self.bot.unload_extension("cogs." + cog)
            self.bot.load_extension("cogs." + cog)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Owner(bot))
