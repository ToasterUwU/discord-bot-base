import os

import nextcord
from nextcord.ext import commands

from internal_tools.configuration import CONFIG
from internal_tools.discord import *


class Owner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_application_command_check(self, interaction: nextcord.Interaction):
        """
        You need to be the Owner of the Bot to use this.
        """
        if interaction.user:
            if isinstance(interaction.user, nextcord.Member):
                user = interaction.user._user
            else:
                user = interaction.user

            return await self.bot.is_owner(user)
        else:
            return False

    @nextcord.slash_command(
        name="owner-cog", guild_ids=CONFIG["GENERAL"]["OWNER_COG_GUILD_IDS"]
    )
    async def topcommand(self, interaction: nextcord.Interaction):
        pass

    @topcommand.subcommand(name="play", description="Sets a 'playing' Status")
    async def play_status(
        self,
        interaction: nextcord.Interaction,
        status: str = nextcord.SlashOption(
            name="status", description="The status text to use", required=True
        ),
    ):
        """
        Sets a 'playing' Status
        """
        await self.bot.change_presence(activity=nextcord.Game(status))
        await interaction.send("Done", ephemeral=True)

    @topcommand.subcommand(name="watch", description="Sets a 'watching' Status")
    async def watch_status(
        self,
        interaction: nextcord.Interaction,
        status: str = nextcord.SlashOption(
            name="status", description="The status text to use", required=True
        ),
    ):
        """
        Sets a 'watching' Status
        """
        await self.bot.change_presence(
            activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=status)
        )
        await interaction.send("Done", ephemeral=True)

    @topcommand.subcommand(name="listen", description="Sets a 'listening' Status")
    async def listen_status(
        self,
        interaction: nextcord.Interaction,
        status: str = nextcord.SlashOption(
            name="status", description="The status text to use", required=True
        ),
    ):
        """
        Sets a 'listening' Status
        """
        await self.bot.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.listening, name=status
            )
        )
        await interaction.send("Done", ephemeral=True)

    async def cog_autocomplete(self, interaction: nextcord.Interaction, cog: str):
        all_cogs = [
            x.name.replace(".py", "")
            for x in os.scandir("cogs/")
            if x.is_file() and not x.name.startswith("_")
        ]

        if cog:
            await interaction.response.send_autocomplete(
                [x for x in all_cogs if x.startswith(cog)]
            )
        else:
            await interaction.response.send_autocomplete(all_cogs)

    @topcommand.subcommand(name="load", description="Loads a Cog")
    async def load_cog(
        self,
        interaction: nextcord.Interaction,
        cog: str = nextcord.SlashOption(
            name="cog",
            description="Name of the Cog you want to load",
            required=True,
            autocomplete_callback=cog_autocomplete,
        ),
    ):
        """
        Loads a Module.
        """
        try:
            self.bot.load_extension("cogs." + cog)
        except Exception as e:
            await interaction.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await interaction.send("Done", ephemeral=True)

    @topcommand.subcommand(name="unload", description="Unloads a Cog")
    async def unload_cog(
        self,
        interaction: nextcord.Interaction,
        cog: str = nextcord.SlashOption(
            name="cog",
            description="Name of the Cog you want to unload",
            required=True,
            autocomplete_callback=cog_autocomplete,
        ),
    ):
        """
        Unloads a Module.
        """
        try:
            self.bot.unload_extension("cogs." + cog)
        except Exception as e:
            await interaction.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await interaction.send("Done", ephemeral=True)

    @topcommand.subcommand(name="reload", description="Reloads a Cog")
    async def reload_cog(
        self,
        interaction: nextcord.Interaction,
        cog: str = nextcord.SlashOption(
            name="cog",
            description="Name of the Cog you want to reload",
            required=True,
            autocomplete_callback=cog_autocomplete,
        ),
    ):
        """
        Reloads a Module.
        """
        try:
            self.bot.unload_extension("cogs." + cog)
            self.bot.load_extension("cogs." + cog)
        except Exception as e:
            await interaction.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await interaction.send("Done", ephemeral=True)

    @topcommand.subcommand(
        name="info", description="Shows info about the Bot and its stats"
    )
    async def show_info_and_stats(self, interaction: nextcord.Interaction):
        await interaction.response.defer()

        guild_amount = 0
        member_amount = 0

        async for g in self.bot.fetch_guilds(limit=None, with_counts=True):
            guild_amount += 1

            if g.approximate_member_count is not None:
                member_amount += g.approximate_member_count  # type: ignore

        embed = fancy_embed(
            title="Stats and Info",
            fields={
                "Server Amount": guild_amount,
                "Approximate User Amount": member_amount,
            },
        )

        await interaction.send(embed=embed)


async def setup(bot):
    bot.add_cog(Owner(bot))
