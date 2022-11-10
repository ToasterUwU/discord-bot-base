# Discord Bot Base

This is a template for a Discord Bot made with nextcord of some sorts.

But not really, since it does more than show a good structure that you can replace. Thats why i called it "Base".

## What it provides

- Solid and modular configuration system that updates existing files from new default files (adds missing config paramaters from default)
- Builtin way of saving data in json files
- Extensive error handler
- internal_tools.discord which includes functions to make live easier (generate embed messages faster, dont fetch if you have it in cache)
- Cog (Commmand group file) that includes commands for the Owner of the Bot. ((un/re)load cog, set a status for the Bot)
- Example Cog that shows some example things, so that you dont have to look at nextcord docs to remember every single little thing.
- Premade setup.iss file for making a Windows installer
- VSCode tasks to clean the workspace of built files
- VSCode tasks to make a .exe file with pyinstaller and built Windows installer from setup.iss
- Preconfigured .gitignore file to exclude all build files and virtual env
- init.py that can be used to automatically make a fresh bot project after providing a name for it (will be created next to the base directory)

## Things to know before using

1. Cogs that start with _ are not loaded on startup, and are hidden from autocomplete in the Owner Cog (Thats how you disable a Cog)
2. The doc string of each Cogs cog_application_command_check is used as a text for error handeling when someone is not allowed to use a Command. (Set it to something that explains whats needed to pass the check)
3. Always put a default value config in the default folder. The actual used configs are not meant to be created by hand.
4. In the GENERAL.json config file, you can set a error webhook url. Thats needed if you want exception traces sent to discord somewhere.
5. Owner Commands only show up in the Server(s) that have their IDs in the OWNER_COG_GUILD_IDS list in the GENERAL.json config. (The standard one is my private testing server)
6. You can set a custom standard color in the GENERAL.json. That will be used as a the color on fancy_embed if you dont set on yourself when using it.
7. If your Bot needs any priveliged intents, you can enable those in the GENERAL.json config file.
8. Your Bot token can either be added manually to the GENERAL.json config file or you can just start the Bot without any setup before that, and it will ask you for the Token

## Other notes

- If you use this, please credit me somehow. I spend a lot of time making this, testing it, refining it. I would feel cheated if someone takes this and just sells it as "their creation".
- If there is anything you want to improve or extend, feel free to make a PR for it. 
- If you found a problem, you are welcome to open an Issue for it.
