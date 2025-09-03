import asyncio
import logging
import os
import sys
from typing import Union

import discord
from discord.ext import commands, tasks

from internal_tools.configuration import CONFIG
from internal_tools.general import error_webhook_send


async def main():
    logger = logging.getLogger("nextcord")
    logger.setLevel(logging.WARNING)
    handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)

    intents = discord.Intents.default()
    intents.members = CONFIG["GENERAL"]["MEMBERS_INTENT"]
    intents.presences = CONFIG["GENERAL"]["PRESENCE_INTENT"]
    intents.message_content = CONFIG["GENERAL"]["MESSAGE_CONTENT_INTENT"]

    bot = commands.Bot(command_prefix=[], intents=intents)

    if CONFIG["GENERAL"]["TOKEN"] == "":
        if len(sys.argv) > 1:
            token = sys.argv[1]
        else:
            token = input(
                "Token is not set in config, please enter the token here.\n\nToken: "
            )

        CONFIG["GENERAL"]["TOKEN"] = token
        CONFIG.save()

    for cog in [
        "cogs." + x.name.replace(".py", "")
        for x in os.scandir("cogs")
        if not x.name.startswith("_")
    ]:
        try:
            await bot.load_extension(cog)
            print(f"Loaded: {cog}")
        except Exception as e:
            print(f"{e}")

    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game("with Slash Commands"))

        print(f"Online and Ready\nLogged in as {bot.user}")

    @discord.app_commands.check(lambda interaction: interaction.user.id == bot.owner_id)
    @discord.app_commands.command(
        name="reload-all",
        description="Reloads all Cogs",
        extras={"guild_id": CONFIG["GENERAL"]["OWNER_COG_GUILD_ID"]},
    )
    async def reload_all_cogs(interaction: discord.Interaction):
        usable_cogs = [
            "cogs." + x.name.replace(".py", "")
            for x in os.scandir("cogs")
            if not x.name.startswith("_")
        ]
        for cog in usable_cogs:
            try:
                await bot.unload_extension(cog)
            except:
                pass

            await bot.load_extension(cog)

        await interaction.response.send_message("Done", ephemeral=True)

    async def _try_send(interaction: discord.Interaction, text: str):
        try:
            await interaction.response.send_message(
                text,
                ephemeral=True,
            )
        except discord.errors.Forbidden:
            return False
        except discord.errors.NotFound:
            return False
        else:
            return True

    @bot.event
    async def on_application_command_error(
        interaction: discord.Interaction,
        exception: discord.errors.DiscordException,
    ):
        if interaction.command:
            if interaction.command.on_error is not None:
                return

        # if isinstance(exception, discord.errors.ApplicationInvokeError):
        #     original_exception = exception.original
        # else:
        #     original_exception = exception

        if isinstance(exception, discord.errors.NotFound):
            if await _try_send(
                interaction,
                "Something being used for this Command (like a channel, member, role, etc.) is missing. It was deleted, or the person left. Fix this issue and try again.",
            ):
                return

        elif isinstance(exception, discord.errors.Forbidden):
            if await _try_send(
                interaction,
                "The Bot is missing permissions for something it has to do for this Command. Make sure it has all needed permissions and try again.",
            ):
                return
            else:
                try:
                    if interaction.user:
                        await interaction.user.send(
                            "The Bot lacks the Permissions needed to send Messages in the Channel you just tried to use a Command in."
                        )
                except:
                    return

        elif isinstance(exception, discord.errors.DiscordServerError):
            if await _try_send(
                interaction,
                "Something went wrong on Discords side. Please try again later.",
            ):
                return

        elif isinstance(
            exception, discord.app_commands.errors.MissingRole
        ):
            if isinstance(exception.missing_role, int):
                missing_role_text = f"<@&{exception.missing_role}>"
            else:
                missing_role_text = f"@{exception.missing_role}"

            if await _try_send(
                interaction,
                f"You are missing the Role that is needed to use this Command. ( {missing_role_text} )",
            ):
                return

        elif isinstance(
            exception, discord.app_commands.errors.MissingAnyRole
        ):
            missing_role_texts = []
            for missing_role in exception.missing_roles:
                if isinstance(missing_role, int):
                    missing_role_texts.append(f"<@&{missing_role}>")
                else:
                    missing_role_texts.append(f"@{missing_role}")

            if await _try_send(
                interaction,
                f"You are missing a Role that is needed to use this Command. ( You need at least on of these: {', '.join(missing_role_texts)} )",
            ):
                return

        elif isinstance(
            exception, discord.app_commands.errors.MissingPermissions
        ):
            if await _try_send(
                interaction,
                f"You lack the Permissions needed to use this Command.\nYou need all of these Permissions: {', '.join(exception.missing_permissions)}",
            ):
                return

        elif isinstance(
            exception,
            discord.app_commands.errors.BotMissingPermissions,
        ):
            if await _try_send(
                interaction,
                f"The Bot lacks the Permissions needed to use this Command.\nThe Bot needs all of these Permissions: {', '.join(exception.missing_permissions)}",
            ):
                return
            else:
                try:
                    if interaction.user:
                        await interaction.user.send(
                            f"The Bot lacks the Permissions needed to send Messages in the Channel you just tried to use a Command in.\nThe Bot needs all of these Permissions: {', '.join(exception.missing_permissions)}"
                        )
                except:
                    return

        elif isinstance(
            exception, discord.app_commands.errors.NoPrivateMessage
        ):
            if await _try_send(
                interaction,
                f"This Command cant be used in DMs. Use it on a Server instead.",
            ):
                return

        await error_webhook_send(exception)

    await bot.start(CONFIG["GENERAL"]["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
