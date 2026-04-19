import discord

class CarouselView(discord.ui.View):
    def __init__(self, parts, author_id):
        super().__init__(timeout=180)
        self.parts = parts
        self.author_id = author_id
        self.index = 0

    async def interaction_check(self, interaction):
        return interaction.user.id == self.author_id

    async def update_message(self, interaction: discord.Interaction):
        content = self.parts[self.index]
        content = f"{self.parts[self.index]}\n\n-# Page {self.index+1}/{len(self.parts)}"
        
        # disable buttons if needed
        self.prev_button.disabled = self.index == 0
        self.next_button.disabled = self.index == len(self.parts) - 1

        await interaction.response.edit_message(
            content=content,
            view=self
        )

    @discord.ui.button(label="⬅ Prev", style=discord.ButtonStyle.secondary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index -= 1
        await self.update_message(interaction)

    @discord.ui.button(label="Next ➡", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index += 1
        await self.update_message(interaction)