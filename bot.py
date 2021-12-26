import logging
import os

import nextcord
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Bot

from config import CONFIG

logging.basicConfig(filename="bot.log", filemode="w+", level=logging.INFO)


intents = nextcord.Intents.default()
# intents.members = True
# intents.presences = True

bot = Bot(CONFIG["DEFAULT"]["PREFIX"], case_insensitivity=True, intents=intents)


if CONFIG["DEFAULT"]["TOKEN"] == "":
    CONFIG["DEFAULT"]["TOKEN"] = input(
        "Token is not set in config.json, please enter the token here.\n\nToken: "
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
    await bot.change_presence(activity=nextcord.Game(f"{CONFIG['DEFAULT']['PREFIX']}help"))

    print(f"Online and Ready\nLogged in as {bot.user}")


@bot.event
async def on_command_error(ctx, error):
    logging.error(f"Error in '{ctx.guild.name}' -> {error}")


@bot.command(name="reload_all", aliases=["reload-all", "reloadall"], hidden=True)
async def reload_all_cogs(ctx):
    if await bot.is_owner(ctx.author):
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

        await ctx.message.add_reaction("✅")


bot.run(CONFIG["DEFAULT"]["TOKEN"])
