import datetime
from typing import List, Optional, Union

import discord

from internal_tools.configuration import CONFIG

__all__ = ["fancy_embed", "GetOrFetch", "CatalogView"]


def CONFIG_EMBED_COLOR():
    """
    Function to give color from the config back
    """
    return discord.Colour(int(CONFIG["GENERAL"]["EMBED_COLOR"].replace("#", ""), 16))


class CatalogView(discord.ui.View):
    def __init__(self, pages: List[discord.Embed], timeout: Optional[float] = 300):
        if len(pages) <= 1:
            raise ValueError(
                "Need at least two pages for this Menu to work and make sense."
            )

        super().__init__(timeout=timeout)

        for i, page in enumerate(pages, start=0):
            page.set_footer(text=f"Page {i+1}/{len(pages)}")

            if i > 0:
                page.add_field(
                    name="Previous Page:", value=f"**{pages[i-1].title}**", inline=False
                )

            if i < len(pages) - 1:
                page.add_field(
                    name="Next Page:", value=f"**{pages[i+1].title}**", inline=False
                )

        self.pages = pages
        self.current_page: int = 0

        self.user: Optional[Union[discord.User, discord.Member]] = None
        self.messsage: discord.Message

    async def show_page(self, number: int):
        if number < 0 or number > len(self.pages) - 1:
            raise ValueError("Index out of range.")

        await self.messsage.edit(embed=self.pages[number])

        self.current_page = number

    async def start(self, interaction: discord.Interaction):
        self.user = interaction.user

        msg = await interaction.response.send_message(
            embed=self.pages[self.current_page], view=self
        )
        if not isinstance(interaction.channel, discord.abc.Messageable):
            raise TypeError("Channel is not Messageable.")

        if msg.message_id is None:
            raise ValueError("Message ID is None.")

        self.messsage = await interaction.channel.fetch_message(msg.message_id)

    async def on_timeout(self) -> None:
        await self.messsage.delete()

        return await super().on_timeout()

    def allowed_to_use(
        self, interaction_user: Optional[Union[discord.User, discord.Member]]
    ):
        if not self.user:
            return True

        return interaction_user == self.user

    @discord.ui.button(label="⏮️", style=discord.ButtonStyle.secondary)
    async def first_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if not self.allowed_to_use(interaction.user):
            await interaction.response.send_message(
                "You are not allowed to use this Catalog.", ephemeral=True
            )
            return

        if self.current_page == 0:
            await interaction.response.send_message("You are already on the first page.", ephemeral=True)
            return

        await self.show_page(0)
        await interaction.response.pong()

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.primary)
    async def previous_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if not self.allowed_to_use(interaction.user):
            await interaction.response.send_message(
                "You are not allowed to use this Catalog.", ephemeral=True
            )
            return

        if self.current_page == 0:
            await interaction.response.send_message("You are already on the first page.", ephemeral=True)
            return

        await self.show_page(self.current_page - 1)
        await interaction.response.pong()

    @discord.ui.button(label="▶️", style=discord .ButtonStyle.primary)
    async def next_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if not self.allowed_to_use(interaction.user):
            await interaction.response.send_message(
                "You are not allowed to use this Catalog.", ephemeral=True
            )
            return

        if self.current_page == len(self.pages) - 1:
            await interaction.response.send_message("You are already on the last page.", ephemeral=True)
            return

        await self.show_page(self.current_page + 1)
        await interaction.response.pong()

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.secondary)
    async def last_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if not self.allowed_to_use(interaction.user):
            await interaction.response.send_message(
                "You are not allowed to use this Catalog.", ephemeral=True
            )
            return

        if self.current_page == len(self.pages) - 1:
            await interaction.response.send_message("You are already on the last page.", ephemeral=True)
            return

        await self.show_page(len(self.pages) - 1)
        await interaction.response.pong()

    @discord.ui.button(label="⏹️", style=discord.ButtonStyle.secondary)
    async def stop_catalog(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if not self.allowed_to_use(interaction.user):
            await interaction.response.send_message(
                "You are not allowed to use this Catalog.", ephemeral=True
            )
            return

        await interaction.response.pong()
        await self.messsage.delete()

        self.stop()


def fancy_embed(
    title: str = "",
    description: str = "",
    fields: dict = {},
    inline: bool = False,
    color: discord.Colour = CONFIG_EMBED_COLOR(),
    footer: Optional[str] = "Made by: @ToasterUwU",
    url: Optional[str] = None,
    timestamp: Optional[datetime.datetime] = None,
    author: Optional[Union[discord.User, discord.Member]] = None,
    image_url: Optional[str] = None,
    thumbnail_url: Optional[str] = None,
):
    """
    Embed generator to save some repeating code
    """
    embed = discord.Embed(
        title=title, description=description, color=color, url=url, timestamp=timestamp
    )
    for name, val in fields.items():
        embed.add_field(name=name, value=val, inline=inline)

    if footer:
        embed.set_footer(text=footer)

    if author:
        embed.set_author(name=author.display_name, icon_url=author.display_avatar.url)

    if image_url:
        embed.set_image(url=image_url)

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    return embed


class GetOrFetch:
    """
    Collection of functions that 'Get or Fetch' things and hide errors, so i dont have to try except all the time.
    """

    @classmethod
    async def guild(cls, bot: discord.Client, id: int):
        guild = bot.get_guild(id)
        if not guild:
            try:
                guild = await bot.fetch_guild(id)
            except:
                pass

        return guild

    @classmethod
    async def channel(
        cls, bot_or_guild: Union[discord.Client, discord.Guild], id: int
    ):
        channel = bot_or_guild.get_channel(id)
        if not channel:
            try:
                channel = await bot_or_guild.fetch_channel(id)
            except:
                pass

        return channel

    @classmethod
    async def role(cls, guild: discord.Guild, id: int):
        role = guild.get_role(id)
        if not role:
            await guild.fetch_roles()
            role = guild.get_role(id)

        return role

    @classmethod
    async def member(cls, guild: discord.Guild, id: int):
        member = guild.get_member(id)
        if not member:
            try:
                member = await guild.fetch_member(id)
            except:
                pass

        return member

    @classmethod
    async def user(cls, bot: discord.Client, id: int):
        user = bot.get_user(id)
        if not user:
            try:
                user = await bot.fetch_user(id)
            except:
                pass

        return user
