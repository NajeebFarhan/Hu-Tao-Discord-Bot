from discord.ext import commands
import discord
from agent.model import chatbot_answer

@commands.command()
async def chat(ctx: commands.Context, *tokens: str, attachments: commands.Greedy[discord.Attachment]) -> None:
    text = " ".join(tokens)
    
    async with ctx.typing():
        answer = chatbot_answer(text, ctx.author.id)
    
    await ctx.reply(answer)