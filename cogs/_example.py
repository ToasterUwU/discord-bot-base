import nextcord
from internal_tools.discord import *
from nextcord.ext import commands


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

    async def cog_application_command_check(self, interaction: nextcord.Interaction):
        """
        Everyone can use this.
        """
        return True

    @nextcord.slash_command(
        name="ask",
        description="Example Command",
        default_member_permissions=nextcord.Permissions(administrator=True),
        dm_permission=False,
    )
    async def ask(self, interaction: nextcord.Interaction):
        """Asks the user a question to confirm something."""
        # We create the view and assign it to a variable so we can wait for it later.
        view = Confirm()
        await interaction.send("Do you want to continue?", view=view)
        # Wait for the View to stop listening for input...
        await view.wait()
        if view.value is None:
            print("Timed out...")
        elif view.value:
            print("Confirmed...")
        else:
            print("Cancelled...")

    @nextcord.slash_command(
        name="localized",
        description="Tests localization.",
        name_localizations={
            nextcord.Locale.en_US: "localized_us",
            "en-GB": "localized_gb",
        },
        description_localizations={
            nextcord.Locale.en_GB: "GB Tests localization.",
            "en-US": "US Tests localization.",
        },
    )
    async def slash_localized(
        self,
        interaction: nextcord.Interaction,
        choice_list: str = nextcord.SlashOption(
            choices=["localized 1", "not localized", "localized 2"],
            choice_localizations={
                "localized 1": {
                    nextcord.Locale.en_US: "US Localized 1",
                    "en-GB": "GB Localized 1",
                },
                "localized 2": {
                    "en-US": "US Localized 2",
                    nextcord.Locale.en_GB: "GB Localized 2",
                },
            },
        ),
    ):
        await interaction.send(
            f"Actual values:\nCmd: `/test localized`, Choice: `{choice_list}`"
        )

    @nextcord.user_command()
    async def my_user_command(
        self, interaction: nextcord.Interaction, member: nextcord.Member
    ):
        await interaction.response.send_message(f"Hello, {member}!")

    @nextcord.message_command()
    async def my_message_command(
        self, interaction: nextcord.Interaction, message: nextcord.Message
    ):
        await interaction.response.send_message(f"{message}")


async def setup(bot):
    bot.add_cog(Example(bot))
