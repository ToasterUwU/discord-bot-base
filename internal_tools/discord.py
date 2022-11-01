import datetime
from typing import Optional, Union

import nextcord

from internal_tools.configuration import CONFIG


def CONFIG_EMBED_COLOR():
    """
    Function to give color from the config back
    """
    return nextcord.Colour(int(CONFIG["GENERAL"]["EMBED_COLOR"].replace("#", ""), 16))


def fancy_embed(
    title: str = "",
    description: str = "",
    fields: dict = {},
    inline: bool = False,
    color: nextcord.Colour = CONFIG_EMBED_COLOR(),
    footer: Optional[str] = "Made by: Aki ToasterUwU#0001",
    url: Optional[str] = None,
    timestamp: Optional[datetime.datetime] = None,
    author: Optional[Union[nextcord.User, nextcord.Member]] = None,
    image_url: Optional[str] = None,
    thumbnail_url: Optional[str] = None,
):
    """
    Embed generator to save some repeating code
    """
    embed = nextcord.Embed(
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


class GetOrFetch:
    """
    Collection of functions that 'Get or Fetch' things and hide errors, so i dont have to try except all the time.
    """

    @classmethod
    async def guild(cls, bot: nextcord.Client, id: int):
        guild = bot.get_guild(id)
        if not guild:
            try:
                guild = await bot.fetch_guild(id)
            except:
                pass

        return guild

    @classmethod
    async def channel(
        cls, bot_or_guild: Union[nextcord.Client, nextcord.Guild], id: int
    ):
        channel = bot_or_guild.get_channel(id)
        if not channel:
            try:
                channel = await bot_or_guild.fetch_channel(id)
            except:
                pass

        return channel

    @classmethod
    async def role(cls, guild: nextcord.Guild, id: int):
        role = guild.get_role(id)
        if not role:
            await guild.fetch_roles(cache=True)
            role = guild.get_role(id)

        return role

    @classmethod
    async def member(cls, guild: nextcord.Guild, id: int):
        member = guild.get_member(id)
        if not member:
            try:
                member = await guild.fetch_member(id)
            except:
                pass

        return member

    @classmethod
    async def user(cls, bot: nextcord.Client, id: int):
        user = bot.get_user(id)
        if not user:
            try:
                user = await bot.fetch_user(id)
            except:
                pass

        return user
