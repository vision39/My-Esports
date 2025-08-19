import discord

class RegistrationView(discord.ui.View):
    def __init__(self, scrim_id: int):
        super().__init__(timeout=None)
        self.scrim_id = scrim_id

    # @discord.ui.button(label="Register", style=discord.ButtonStyle.green, custom_id="register_button")
    # async def register_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     """
    #     This button will be attached to the scrim registration message.
    #     When a user clicks it, we will open a modal (a pop-up form)
    #     to ask for their team name and player tags.
    #     """
    #     pass

    # We will add other buttons here later, like "View Slot List" or "Cancel Registration".
