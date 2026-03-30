import discord
from discord.ext import commands
from discord.ui import View, Button
from agent.libs.history import show_history

MAX_CHARS = 60
TURNS_PER_PAGE = 5


def truncate(text: str, limit=MAX_CHARS):
    text = text.replace("\n", " ")
    return text[:limit] + ("..." if len(text) > limit else "")


def format_human_message(content: list[dict]):

    text_part = content[0]["text"]

    has_image = any(
        part.get("type") == "image_url"
        for part in content
    )

    result = truncate(text_part)

    if has_image:
        result += " [contains image(s)]"

    return result


def group_turns(messages: list):

    turns = []
    current_turn = None

    for m in messages:
        m = m.model_dump()
        
        if m["type"] == "human":
            
            if current_turn:
                turns.append(current_turn)

            if type(m["content"]) == str:
                current_turn = {
                    "human": truncate(m["content"]),
                    "ai": []
                }
                
            else:
                current_turn = {
                    "human": format_human_message(m["content"]),
                    "ai": []
                }

        elif m["type"] == "ai":

            if current_turn:
                current_turn["ai"].append(
                    truncate(m["content"])
                )

        # tool messages skipped completely

    if current_turn:
        turns.append(current_turn)

    return turns


class HistoryView(View):

    def __init__(self, name, turns, page=0):
        super().__init__(timeout=120)
        
        self.name = name
        self.turns = turns
        self.page = page

        self.update_buttons()


    def update_buttons(self):

        self.clear_items()

        if self.page > 0:

            self.add_item(
                Button(
                    label="Previous",
                    style=discord.ButtonStyle.secondary,
                    custom_id="prev"
                )
            )

        if (self.page + 1) * TURNS_PER_PAGE < len(self.turns):

            self.add_item(
                Button(
                    label="Next",
                    style=discord.ButtonStyle.primary,
                    custom_id="next"
                )
            )


    async def interaction_check(self, interaction):

        if interaction.data["custom_id"] == "prev":
            self.page -= 1

        elif interaction.data["custom_id"] == "next":
            self.page += 1

        embed = create_embed(self.name, self.turns, self.page)

        self.update_buttons()

        await interaction.response.edit_message(
            embed=embed,
            view=self
        )

        return False


def create_embed(name: str, turns: list, page: int):

    start = page * TURNS_PER_PAGE
    end = start + TURNS_PER_PAGE

    selected = turns[start:end]

    embed = discord.Embed(
        title=f"{name}'s Chat History",
        description=f"Page {page+1}/{(len(turns)-1)//TURNS_PER_PAGE+1}",
        color=discord.Color.blurple()
    )

    for i, turn in enumerate(selected, start=start+1):

        ai_text = "\n".join(turn["ai"]) if turn["ai"] else "*No response*"

        embed.add_field(
            name=f"{i}.",
            value=(
                f"**User:** {turn['human']}\n"
                f"**AI:** {ai_text}"
            ),
            inline=False
        )

    return embed


import os

@commands.command()
async def history(ctx: commands.Context, user_id: int | None = None):
    thread_id = ctx.author.id
    
    if user_id and str(ctx.author.id) == os.environ["OWNER_ID"]:
        thread_id = user_id
    else:
        await ctx.send("Only the owner can look into other user's chat history")
        return
    
    try:     
        user = await ctx.bot.fetch_user(thread_id)

        messages = show_history(thread_id)

        turns = group_turns(messages)[::-1]

        if not turns:
            await ctx.send("No chat history found.")
            return

        view = HistoryView(user.name, turns)

        embed = create_embed(user.name, turns, 0)

        await ctx.send(embed=embed, view=view)
        
    except:
        await ctx.send("Something went wrong")