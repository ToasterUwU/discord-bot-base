import logging
import os
import sys

import interactions

from internal_tools.configuration import CONFIG
from internal_tools.general import error_webhook_send

if __name__ == "__main__":
    logger = logging.getLogger("DiscordBot")
    logger.setLevel(logging.WARNING)
    handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)

    intents = interactions.Intents.DEFAULT
    if CONFIG["GENERAL"]["MEMBERS_INTENT"]:
        intents = intents | interactions.Intents.GUILD_MEMBERS
    if CONFIG["GENERAL"]["PRESENCE_INTENT"]:
        intents = intents | interactions.Intents.GUILD_PRESENCES
    if CONFIG["GENERAL"]["MESSAGE_CONTENT_INTENT"]:
        intents = intents | interactions.Intents.MESSAGE_CONTENT

    bot = interactions.Client(intents=intents)

    if CONFIG["GENERAL"]["TOKEN"] == "":
        if len(sys.argv) > 1:
            token = sys.argv[1]
        else:
            token = input(
                "Token is not set in config, please enter the token here.\n\nToken: "
            )

        CONFIG["GENERAL"]["TOKEN"] = token
        CONFIG.save()

    for extension in [
        "extensions." + x.name.replace(".py", "")
        for x in os.scandir("extensions")
        if not x.name.startswith("_")
    ]:
        try:
            bot.load_extension(extension)
            print(f"Loaded: {extension}")
        except Exception as e:
            print(f"{e}")

    @interactions.listen()
    async def on_startup():
        await bot.change_presence(activity=interactions.Activity("with Slash Commands"))

        print(f"Online and Ready\nLogged in as {bot.user}")

    @interactions.slash_command(
        name="reload-all",
        description="Reloads all Extensions",
        scopes=CONFIG["GENERAL"]["OWNER_EXTENSION_GUILD_IDS"],
    )
    @interactions.check(interactions.is_owner())
    async def reload_all_extensions(interaction: interactions.SlashContext):
        usable_extensions = [
            "extensions." + x.name.replace(".py", "")
            for x in os.scandir("extensions")
            if not x.name.startswith("_")
        ]
        for extension in usable_extensions:
            try:
                bot.unload_extension(extension)
            except:
                pass

            bot.load_extension(extension)

        await interaction.send("Done", ephemeral=True)

    async def _try_send(interaction: interactions.SlashContext, text: str):
        try:
            await interaction.send(
                text,
                ephemeral=True,
            )
        except interactions.errors.Forbidden:
            return False
        except interactions.errors.NotFound:
            return False
        else:
            return True

    @interactions.listen(interactions.api.events.CommandError)
    async def on_command_error(
        ctx: interactions.SlashContext,
        exception: Exception,
    ):
        if ctx.command is not None:
            if ctx.command.error_callback is not None:
                return

        if isinstance(exception, interactions.errors.NotFound):
            if await _try_send(
                ctx,
                "Something being used for this Command (like a channel, member, role, etc.) is missing. It was deleted, or the person left. Fix this issue and try again.",
            ):
                return

        elif isinstance(exception, interactions.errors.Forbidden):
            if await _try_send(
                ctx,
                "The Bot is missing permissions for something it has to do for this Command. Make sure it has all needed permissions and try again.",
            ):
                return
            else:
                try:
                    if ctx.user:
                        await ctx.user.send(
                            "The Bot lacks the Permissions needed to send Messages in the Channel you just tried to use a Command in."
                        )
                except:
                    return

        elif isinstance(exception, interactions.errors.DiscordError):
            if await _try_send(
                ctx,
                "Something went wrong on Discords side. Please try again later.",
            ):
                return

        elif isinstance(exception, interactions.errors.CommandCheckFailure):
            if await _try_send(
                ctx,
                "You are missing a Requirement to use this Command. This could be being the Owner of the Bot, having a certain Role, Permission, only being allowed to use this command in a specific channel, etc.",
            ):
                return

        await error_webhook_send(exception, bot)

    bot.start(CONFIG["GENERAL"]["TOKEN"])
