import asyncio
from discord.ext import commands
import discord
from agent.libs.chatbot_answer import chatbot_answer
from libs.logger import log_command_error
from libs.truncate import truncate

@commands.command()
async def chat(ctx: commands.Context, *tokens: str, attachments: commands.Greedy[discord.Attachment]) -> None:
    # if int(os.environ["OWNER_ID"]) != ctx.author.id:
    #     await ctx.reply("Sorry, this command is temporary unavailable.", mention_author=False)
    #     return
    
    text = " ".join(tokens)

    try:
        async with ctx.typing():
            # Run synchronous LLM call in a worker thread so Discord heartbeats stay responsive.
            answer = await asyncio.to_thread(chatbot_answer, text, ctx.author.id, attachments)
            
        answer = truncate(answer, 1995)

        await ctx.reply(answer, mention_author=False)
        
    except Exception as e:
        log_command_error(ctx, e)
        await ctx.reply("Something went wrong", mention_author=False)