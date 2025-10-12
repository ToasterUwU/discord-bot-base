# from typing import Optional

# import interactions


# class Confirm(interactions.ActionRow):
#     def __init__(self):
#         super().__init__()
#         self.value = None

#     # When the confirm button is pressed, set the inner value to `True` and
#     # stop the View from listening to more input.
#     # We also send the user an ephemeral message that we're confirming their choice.
#     confirm_btn = interactions.Button(
#         style=interactions.ButtonStyle.SUCCESS, label="Confirm", custom_id="confirm"
#     )

#     @interactions.component_callback("confirm")
#     async def confirm(self, ctx: interactions.ComponentContext):
#         await ctx.send("Confirming", ephemeral=True)
#         self.value = True

#     # This one is similar to the confirmation button except sets the inner value to `False`
#     cancel_btn = interactions.Button(
#         style=interactions.ButtonStyle.DANGER, label="Cancel", custom_id="cancel"
#     )

#     @interactions.component_callback("cancel")
#     async def cancel(self, ctx: interactions.ComponentContext):
#         await ctx.send("Cancelling", ephemeral=True)
#         self.value = False


# class Example(interactions.Extension):
#     def __init__(self):
#         super().__init__()

#         self.add_ext_check(self.extension_command_check)

#     @staticmethod
#     async def extension_command_check(ctx: interactions.BaseContext):
#         """
#         Everyone can use this.
#         """
#         return True

#     def ask_check(self):
#         """
#         Check if the user is the one who started the interaction.
#         """

#         async def predicate(ctx: interactions.SlashContext):
#             return ctx.user.id == ctx.author.id

#         return predicate

#     @interactions.slash_command(
#         name="ask",
#         description="Example Command",
#         default_member_permissions=interactions.Permissions.ADMINISTRATOR,
#         contexts=[interactions.ContextType.GUILD],
#     )
#     async def ask(self, interaction: interactions.SlashContext):
#         """Asks the user a question to confirm something."""
#         # We create the view and assign it to a variable so we can wait for it later.
#         action_row = Confirm()
#         msg = await interaction.send("Do you want to continue?", components=action_row)
#         action_row.msg = msg
#         # Wait for the View to stop listening for input...
#         await view.wait()
#         if view.value is None:
#             print("Timed out...")
#         elif view.value:
#             print("Confirmed...")
#         else:
#             print("Cancelled...")

#     @nextcord.slash_command(
#         name="localized",
#         description="Tests localization.",
#         name_localizations={
#             nextcord.Locale.en_US: "localized_us",
#             "en-GB": "localized_gb",
#         },
#         description_localizations={
#             nextcord.Locale.en_GB: "GB Tests localization.",
#             "en-US": "US Tests localization.",
#         },
#     )
#     async def slash_localized(
#         self,
#         interaction: nextcord.Interaction,
#         choice_list: str = nextcord.SlashOption(
#             choices=["localized 1", "not localized", "localized 2"],
#             choice_localizations={
#                 "localized 1": {
#                     nextcord.Locale.en_US: "US Localized 1",
#                     "en-GB": "GB Localized 1",
#                 },
#                 "localized 2": {
#                     "en-US": "US Localized 2",
#                     nextcord.Locale.en_GB: "GB Localized 2",
#                 },
#             },
#         ),
#     ):
#         await interaction.send(
#             f"Actual values:\nCmd: `/test localized`, Choice: `{choice_list}`"
#         )

#     @nextcord.user_command()
#     async def my_user_command(
#         self, interaction: nextcord.Interaction, member: nextcord.Member
#     ):
#         await interaction.response.send_message(f"Hello, {member}!")

#     @nextcord.message_command()
#     async def my_message_command(
#         self, interaction: nextcord.Interaction, message: nextcord.Message
#     ):
#         await interaction.response.send_message(f"{message}")


# async def setup(bot):
#     bot.add_extension(Example(bot))
