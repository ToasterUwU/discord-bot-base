import os

import interactions

from internal_tools.configuration import CONFIG
from internal_tools.discord import fancy_embed


class Owner(interactions.Extension):
    def __init__(self, bot: interactions.Client):
        self.add_ext_check(interactions.is_owner())

        _ = self.load_extension.autocomplete("extension")(self.extension_autocomplete)
        _ = self.unload_extension.autocomplete("extension")(self.extension_autocomplete)
        _ = self.reload_extension.autocomplete("extension")(self.extension_autocomplete)

    async def extension_autocomplete(
        self, ctx: interactions.AutocompleteContext, extension: str
    ):
        all_extensions = [
            x.name.replace(".py", "")
            for x in os.scandir("extensions/")
            if x.is_file() and not x.name.startswith("_")
        ]

        if extension:
            await ctx.send(
                choices=[x for x in all_extensions if x.startswith(extension)]
            )
        else:
            await ctx.send(choices=all_extensions)

    @interactions.slash_command(
        name="owner-extension", scopes=CONFIG["GENERAL"]["OWNER_EXTENSION_GUILD_IDS"]
    )
    async def topcommand(self, interaction: interactions.SlashContext):
        pass

    @topcommand.subcommand(
        sub_cmd_name="play", sub_cmd_description="Sets a 'playing' Status"
    )
    @interactions.slash_option(
        name="status",
        description="The status text to use",
        required=True,
        opt_type=interactions.OptionType.STRING,
    )
    async def play_status(
        self,
        ctx: interactions.SlashContext,
        status: str,
    ):
        """
        Sets a 'playing' Status
        """
        await self.bot.change_presence(activity=interactions.Activity(status))
        await ctx.send("Done", ephemeral=True)

    @topcommand.subcommand(
        sub_cmd_name="watch", sub_cmd_description="Sets a 'watching' Status"
    )
    @interactions.slash_option(
        name="status",
        description="The status text to use",
        required=True,
        opt_type=interactions.OptionType.STRING,
    )
    async def watch_status(
        self,
        ctx: interactions.SlashContext,
        status: str,
    ):
        """
        Sets a 'watching' Status
        """
        await self.bot.change_presence(
            activity=interactions.Activity(
                type=interactions.ActivityType.WATCHING, name=status
            )
        )
        await ctx.send("Done", ephemeral=True)

    @topcommand.subcommand(
        sub_cmd_name="listen", sub_cmd_description="Sets a 'listening' Status"
    )
    @interactions.slash_option(
        name="status",
        description="The status text to use",
        required=True,
        opt_type=interactions.OptionType.STRING,
    )
    async def listen_status(
        self,
        ctx: interactions.SlashContext,
        status: str,
    ):
        """
        Sets a 'listening' Status
        """
        await self.bot.change_presence(
            activity=interactions.Activity(
                type=interactions.ActivityType.LISTENING, name=status
            )
        )
        await ctx.send("Done", ephemeral=True)

    @topcommand.subcommand(sub_cmd_name="load", sub_cmd_description="Loads a Extension")
    @interactions.slash_option(
        name="extension",
        description="Name of the Extension you want to load",
        required=True,
        opt_type=interactions.OptionType.STRING,
        autocomplete=True,
    )
    async def load_extension(self, ctx: interactions.SlashContext, extension: str):
        """
        Loads a Extension.
        """
        try:
            self.bot.load_extension("extensions." + extension)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("Done", ephemeral=True)

    @topcommand.subcommand(
        sub_cmd_name="unload", sub_cmd_description="Unloads a Extension"
    )
    @interactions.slash_option(
        name="extension",
        description="Name of the Extension you want to load",
        required=True,
        opt_type=interactions.OptionType.STRING,
        autocomplete=True,
    )
    async def unload_extension(
        self,
        ctx: interactions.SlashContext,
        extension: str,
    ):
        """
        Unloads a Extension.
        """
        try:
            self.bot.unload_extension("extensions." + extension)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("Done", ephemeral=True)

    @topcommand.subcommand(
        sub_cmd_name="reload", sub_cmd_description="Reloads a Extension"
    )
    @interactions.slash_option(
        name="extension",
        description="Name of the Extension you want to load",
        required=True,
        opt_type=interactions.OptionType.STRING,
        autocomplete=True,
    )
    async def reload_extension(
        self,
        ctx: interactions.SlashContext,
        extension: str,
    ):
        """
        Reloads a Extension.
        """
        try:
            self.bot.unload_extension("extensions." + extension)
            self.bot.load_extension("extensions." + extension)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("Done", ephemeral=True)

    @topcommand.subcommand(
        sub_cmd_name="info",
        sub_cmd_description="Shows info about the Bot and its stats",
    )
    async def show_info_and_stats(self, ctx: interactions.SlashContext):
        await ctx.defer()

        guild_amount = 0
        member_amount = 0

        for g in self.bot.guilds:
            guild_amount += 1

            if g.member_count is not None:
                member_amount += g.member_count

        embed = fancy_embed(
            title="Stats and Info",
            fields={
                "Server Amount": guild_amount,
                "Approximate User Amount": member_amount,
            },
        )

        await ctx.send(embed=embed)
