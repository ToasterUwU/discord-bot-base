import nextcord

from internal_tools.configuration import CONFIG


def CONFIG_EMBED_COLOR():
    return nextcord.Colour(int(CONFIG["DEFAULT"]["EMBED_COLOR"].replace("#", ""), 16))


def fancy_embed(
    title="", description="", fields={}, color=CONFIG_EMBED_COLOR(), inline=False
):
    embed = nextcord.Embed(title=title, description=description, color=color)
    for name, val in fields.items():
        embed.add_field(name=name, value=val, inline=inline)
    embed.set_footer(text="Made by: Aki ToasterUwU#0001")

    return embed
