from typing import Optional, Union

import interactions

from internal_tools.configuration import CONFIG

__all__ = ["fancy_embed"]


def CONFIG_EMBED_COLOR():
    """
    Function to give color from the config back
    """
    return interactions.Color(
        int(CONFIG["GENERAL"]["EMBED_COLOR"].replace("#", ""), 16)
    )


def fancy_embed(
    title: str = "",
    description: str = "",
    fields: dict = {},
    inline: bool = False,
    color: interactions.Color = CONFIG_EMBED_COLOR(),
    footer: Optional[str] = "Made by: @ToasterUwU",
    url: Optional[str] = None,
    timestamp: Optional[interactions.Timestamp] = None,
    author: Optional[Union[interactions.User, interactions.Member]] = None,
    image_url: Optional[str] = None,
    thumbnail_url: Optional[str] = None,
):
    """
    Embed generator to save some repeating code
    """
    embed = interactions.Embed(
        title=title, description=description, color=color, url=url, timestamp=timestamp
    )
    for name, val in fields.items():
        embed.add_field(name=name, value=val, inline=inline)

    if footer:
        embed.set_footer(text=footer)

    if author:
        embed.set_author(name=author.display_name, icon_url=author.display_avatar.url)

    if image_url:
        embed.set_image(image_url)

    if thumbnail_url:
        embed.set_thumbnail(thumbnail_url)

    return embed