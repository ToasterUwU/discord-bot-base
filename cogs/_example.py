import nextcord
from nextcord.ext import commands

from ._functions import *


class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.green)
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.send_message("Confirming", ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.grey)
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.send_message("Cancelling", ephemeral=True)
        self.value = False
        self.stop()


class Example(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def ask(self, ctx: commands.Context):
        """Asks the user a question to confirm something."""
        # We create the view and assign it to a variable so we can wait for it later.
        view = Confirm()
        await ctx.send("Do you want to continue?", view=view)
        # Wait for the View to stop listening for input...
        await view.wait()
        if view.value is None:
            print("Timed out...")
        elif view.value:
            print("Confirmed...")
        else:
            print("Cancelled...")


def setup(bot):
    bot.add_cog(Example(bot))
