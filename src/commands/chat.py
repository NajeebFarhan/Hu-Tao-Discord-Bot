from discord.ext import commands
import discord
from agent.model import chatbot_answer
import os
import asyncio

@commands.command()
async def chat(ctx: commands.Context, *tokens: str, attachments: commands.Greedy[discord.Attachment]) -> None:
    # if int(os.environ["OWNER_ID"]) != ctx.author.id:
    #     await ctx.reply("Sorry, this command is temporary unavailable.", mention_author=False)
    #     return
    
    text = " ".join(tokens)
    
    await ctx.typing()
    
    print(text)
    answer = chatbot_answer(text, ctx.author.id, attachments)
    print(answer)

    await ctx.reply(answer)