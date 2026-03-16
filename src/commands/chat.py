from discord.ext import commands
import discord
from agent.model import chatbot_answer
import os

@commands.command()
async def chat(ctx: commands.Context, *tokens: str, attachments: commands.Greedy[discord.Attachment]) -> None:
    if int(os.environ["OWNER_ID"]) != ctx.author.id:
        await ctx.reply("Sorry, this command is temporary unavailable.", mention_author=False)
    
    text = " ".join(tokens)
    
    async with ctx.typing():
        answer = chatbot_answer(text, ctx.author.id, attachments)

    await ctx.reply(answer)
    # await ctx.reply("test reply")