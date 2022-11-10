import asyncio
import logging
import os
import traceback
from typing import Union

import aiohttp
import nextcord
from nextcord.ext import application_checks, commands, tasks

from internal_tools.configuration import CONFIG


async def main():
    logging.basicConfig(filename="bot.log", filemode="w+", level=logging.INFO)

    intents = nextcord.Intents.default()
    intents.members = CONFIG["GENERAL"]["MEMBERS_INTENT"]
    intents.presences = CONFIG["GENERAL"]["PRESENCE_INTENT"]
    intents.message_content = CONFIG["GENERAL"]["MESSAGE_CONTENT_INTENT"]

    bot = commands.Bot(intents=intents)

    if CONFIG["GENERAL"]["TOKEN"] == "":
        CONFIG["GENERAL"]["TOKEN"] = input(
            "Token is not set in config, please enter the token here.\n\nToken: "
        )
        CONFIG.save()

    for cog in [
        "cogs." + x.name.replace(".py", "")
        for x in os.scandir("cogs")
        if not x.name.startswith("_")
    ]:
        try:
            bot.load_extension(cog)
            print(f"Loaded: {cog}")
        except Exception as e:
            print(f"{e}")

    @bot.event
    async def on_ready():
        await bot.change_presence(activity=nextcord.Game("with Slash Commands"))

        print(f"Online and Ready\nLogged in as {bot.user}")

    @bot.slash_command(
        name="reload-all",
        description="Reloads all Cogs",
        guild_ids=CONFIG["GENERAL"]["OWNER_COG_GUILD_IDS"],
    )
    @application_checks.is_owner()
    async def reload_all_cogs(interaction: nextcord.Interaction):
        usable_cogs = [
            "cogs." + x.name.replace(".py", "")
            for x in os.scandir("cogs")
            if not x.name.startswith("_")
        ]
        for cog in usable_cogs:
            try:
                bot.unload_extension(cog)
            except:
                pass

            bot.load_extension(cog)

        await interaction.send("Done", ephemeral=True)

    async def _try_send(interaction: nextcord.Interaction, text: str):
        try:
            await interaction.send(
                text,
                ephemeral=True,
            )
        except nextcord.errors.Forbidden:
            return False
        except nextcord.errors.NotFound:
            return False
        else:
            return True

    @bot.event
    async def on_application_command_error(
        interaction: nextcord.Interaction,
        exception: Union[
            nextcord.errors.ApplicationInvokeError,
            nextcord.errors.ApplicationCheckFailure,
        ],
    ):
        if interaction.application_command:
            if interaction.application_command.error_callback != None:
                return

        if isinstance(exception, nextcord.errors.ApplicationInvokeError):
            original_exception = exception.original
        else:
            original_exception = exception

        if isinstance(
            original_exception, application_checks.errors.ApplicationCheckAnyFailure
        ):
            original_exception = original_exception.errors[
                0
            ]  # Take the first problem and show it. Step by step.

        if isinstance(original_exception, nextcord.errors.NotFound):
            if await _try_send(
                interaction,
                "Something being used for this Command (like a channel, member, role, etc.) is missing. It was deleted, or the person left. Fix this issue and try again.",
            ):
                return

        elif isinstance(original_exception, nextcord.errors.Forbidden):
            if await _try_send(
                interaction,
                "The Bot is missing permissions for something it has to do for this Command. Make sure it has all needed permissions and try again.",
            ):
                return
            else:
                try:
                    if interaction.user:
                        await interaction.user.send(
                            f"The Bot lacks the Permissions needed to send Messages in the Channel you just tried to use a Command in."
                        )
                except:
                    return

        elif isinstance(original_exception, nextcord.errors.DiscordServerError):
            if await _try_send(
                interaction,
                "Something went wrong on Discords side. Please try again later.",
            ):
                return

        elif isinstance(
            original_exception, application_checks.errors.ApplicationMissingRole
        ):
            if type(original_exception.missing_role) == int:
                missing_role_text = f"<@&{original_exception.missing_role}>"
            else:
                missing_role_text = f"@{original_exception.missing_role}"

            if await _try_send(
                interaction,
                f"You are missing the Role that is needed to use this Command. ( {missing_role_text} )",
            ):
                return

        elif isinstance(
            original_exception, application_checks.errors.ApplicationMissingAnyRole
        ):
            missing_role_texts = []
            for missing_role in original_exception.missing_roles:
                if type(missing_role) == int:
                    missing_role_texts.append(f"<@&{missing_role}>")
                else:
                    missing_role_texts.append(f"@{missing_role}")

            if await _try_send(
                interaction,
                f"You are missing a Role that is needed to use this Command. ( You need at least on of these: {', '.join(missing_role_texts)} )",
            ):
                return

        elif isinstance(
            original_exception, application_checks.errors.ApplicationBotMissingRole
        ):
            if type(original_exception.missing_role) == int:
                missing_role_text = f"<@&{original_exception.missing_role}>"
            else:
                missing_role_text = f"@{original_exception.missing_role}"

            if await _try_send(
                interaction,
                f"The Bot is missing the Role that is needed to use this Command. ( {missing_role_text} )",
            ):
                return

        elif isinstance(
            original_exception, application_checks.errors.ApplicationBotMissingAnyRole
        ):
            missing_role_texts = []
            for missing_role in original_exception.missing_roles:
                if type(missing_role) == int:
                    missing_role_texts.append(f"<@&{missing_role}>")
                else:
                    missing_role_texts.append(f"@{missing_role}")

            if await _try_send(
                interaction,
                f"The Bot is missing a Role that is needed to use this Command. ( The Bot needs at least on of these: {', '.join(missing_role_texts)} )",
            ):
                return

        elif isinstance(
            original_exception, application_checks.errors.ApplicationMissingPermissions
        ):
            if await _try_send(
                interaction,
                f"You lack the Permissions needed to use this Command.\nYou need all of these Permissions: {', '.join(original_exception.missing_permissions)}",
            ):
                return

        elif isinstance(
            original_exception,
            application_checks.errors.ApplicationBotMissingPermissions,
        ):
            if await _try_send(
                interaction,
                f"The Bot lacks the Permissions needed to use this Command.\nThe Bot needs all of these Permissions: {', '.join(original_exception.missing_permissions)}",
            ):
                return
            else:
                try:
                    if interaction.user:
                        await interaction.user.send(
                            f"The Bot lacks the Permissions needed to send Messages in the Channel you just tried to use a Command in.\nThe Bot needs all of these Permissions: {', '.join(original_exception.missing_permissions)}"
                        )
                except:
                    return

        elif isinstance(
            original_exception, application_checks.errors.ApplicationNoPrivateMessage
        ):
            if await _try_send(
                interaction,
                f"This Command cant be used in DMs. Use it on a Server instead.",
            ):
                return

        elif isinstance(
            original_exception,
            application_checks.errors.ApplicationPrivateMessageOnly,
        ):
            if await _try_send(
                interaction,
                f"This Command can only be used in DMs.",
            ):
                return

        elif isinstance(
            original_exception,
            application_checks.errors.ApplicationNotOwner,
        ):
            if await _try_send(
                interaction,
                f"You need to be the Owner of this Bot to use this Command.",
            ):
                return

        elif isinstance(
            original_exception,
            application_checks.errors.ApplicationNSFWChannelRequired,
        ):
            if original_exception.channel:
                channel_mention = f"<#{original_exception.channel.id}>"
            else:
                channel_mention = f"The Channel used for this Command"

            if await _try_send(
                interaction,
                f"{channel_mention} needs to be a NSFW Channel. You can make it one in the Channel settings.",
            ):
                return

        elif isinstance(
            original_exception,
            application_checks.errors.ApplicationCheckForBotOnly,
        ):
            if await _try_send(
                interaction,
                f"This Command is only usable for other Bots.",
            ):
                return

        elif isinstance(original_exception, nextcord.errors.ApplicationCheckFailure):
            try:
                doc_string = interaction.application_command.parent_cog.cog_application_command_check.__doc__.strip("\n ")  # type: ignore
            except:
                doc_string = ""

            if await _try_send(
                interaction,
                f"You are not allowed to use this Command.\n{doc_string}",
            ):
                return

        if CONFIG["GENERAL"]["ERROR_WEBHOOK_URL"]:
            webhook = nextcord.Webhook.from_url(
                CONFIG["GENERAL"]["ERROR_WEBHOOK_URL"], session=aiohttp.ClientSession()
            )

            text = "".join(traceback.format_exception(original_exception))
            await webhook.send(f"Unpredicted Error:\n```\n{text}\n```")

    await bot.start(CONFIG["GENERAL"]["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
