import datetime
from typing import List, Optional, Union

import nextcord

from internal_tools.configuration import CONFIG

__all__ = ["fancy_embed", "GetOrFetch", "CatalogView"]


def CONFIG_EMBED_COLOR():
    """
    Function to give color from the config back
    """
    return nextcord.Colour(int(CONFIG["GENERAL"]["EMBED_COLOR"].replace("#", ""), 16))


class CatalogView(nextcord.ui.View):
    def __init__(self, pages: List[nextcord.Embed], timeout: Optional[float] = 300):
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

        self.user: Optional[Union[nextcord.User, nextcord.Member]] = None
        self.messsage: nextcord.Message

    async def show_page(self, number: int):
        if number < 0 or number > len(self.pages) - 1:
            raise ValueError("Index out of range.")

        await self.messsage.edit(embed=self.pages[number])

        self.current_page = number

    async def start(self, interaction: nextcord.Interaction):
        self.user = interaction.user

        msg = await interaction.response.send_message(
            embed=self.pages[self.current_page], view=self
        )
        self.messsage = await msg.fetch()

    async def on_timeout(self) -> None:
        await self.messsage.delete()

        return await super().on_timeout()

    def allowed_to_use(
        self, interaction_user: Optional[Union[nextcord.User, nextcord.Member]]
    ):
        if not self.user:
            return True

        return interaction_user == self.user

    @nextcord.ui.button(label="⏮️", style=nextcord.ButtonStyle.secondary)
    async def first_page(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if not self.allowed_to_use(interaction.user):
            await interaction.send(
                "You are not allowed to use this Catalog.", ephemeral=True
            )
            return

        if self.current_page == 0:
            await interaction.send("You are already on the first page.", ephemeral=True)
            return

        await self.show_page(0)
        await interaction.response.pong()

    @nextcord.ui.button(label="◀️", style=nextcord.ButtonStyle.primary)
    async def previous_page(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if not self.allowed_to_use(interaction.user):
            await interaction.send(
                "You are not allowed to use this Catalog.", ephemeral=True
            )
            return

        if self.current_page == 0:
            await interaction.send("You are already on the first page.", ephemeral=True)
            return

        await self.show_page(self.current_page - 1)
        await interaction.response.pong()

    @nextcord.ui.button(label="▶️", style=nextcord.ButtonStyle.primary)
    async def next_page(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if not self.allowed_to_use(interaction.user):
            await interaction.send(
                "You are not allowed to use this Catalog.", ephemeral=True
            )
            return

        if self.current_page == len(self.pages) - 1:
            await interaction.send("You are already on the last page.", ephemeral=True)
            return

        await self.show_page(self.current_page + 1)
        await interaction.response.pong()

    @nextcord.ui.button(label="⏭️", style=nextcord.ButtonStyle.secondary)
    async def last_page(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if not self.allowed_to_use(interaction.user):
            await interaction.send(
                "You are not allowed to use this Catalog.", ephemeral=True
            )
            return

        if self.current_page == len(self.pages) - 1:
            await interaction.send("You are already on the last page.", ephemeral=True)
            return

        await self.show_page(len(self.pages) - 1)
        await interaction.response.pong()

    @nextcord.ui.button(label="⏹️", style=nextcord.ButtonStyle.secondary)
    async def stop_catalog(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if not self.allowed_to_use(interaction.user):
            await interaction.send(
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
