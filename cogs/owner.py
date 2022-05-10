import nextcord
from nextcord.ext import commands

from internal_tools.discord import *
from internal_tools.configuration import CONFIG


class Owner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_application_command_check(self, interaction: nextcord.Interaction):
        if await self.bot.is_owner(interaction.user):
            return True
        else:
            await interaction.send(
                "You are not allowed to use this Command", ephemeral=True
            )
            return False

    @nextcord.slash_command(
        name="play",
        description="Sets a 'playing' Status",
        guild_ids=CONFIG["DEFAULT"]["OWNER_COG_GUILD_ID"],
    )
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

    @nextcord.slash_command(
        name="watch",
        description="Sets a 'watching' Status",
        guild_ids=CONFIG["DEFAULT"]["OWNER_COG_GUILD_ID"],
    )
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

    @nextcord.slash_command(
        name="listen",
        description="Sets a 'listening' Status",
        guild_ids=CONFIG["DEFAULT"]["OWNER_COG_GUILD_ID"],
    )
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

    @nextcord.slash_command(
        name="load",
        description="Loads a Cog",
        guild_ids=CONFIG["DEFAULT"]["OWNER_COG_GUILD_ID"],
    )
    async def load_cog(
        self,
        interaction: nextcord.Interaction,
        cog: str = nextcord.SlashOption(
            name="cog", description="Name of the Cog you want to load", required=True
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

    @nextcord.slash_command(
        name="unload",
        description="Loads a Cog",
        guild_ids=CONFIG["DEFAULT"]["OWNER_COG_GUILD_ID"],
    )
    async def unload_cog(
        self,
        interaction: nextcord.Interaction,
        cog: str = nextcord.SlashOption(
            name="cog", description="Name of the Cog you want to unload", required=True
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

    @nextcord.slash_command(
        name="reload",
        description="Reloads a Cog",
        guild_ids=CONFIG["DEFAULT"]["OWNER_COG_GUILD_ID"],
    )
    async def reload_cog(
        self,
        interaction: nextcord.Interaction,
        cog: str = nextcord.SlashOption(
            name="cog", description="Name of the Cog you want to reload", required=True
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


def setup(bot):
    bot.add_cog(Owner(bot))
