from discord.ext import commands
import discord
from agent.libs.chatbot_answer import chatbot_answer


@commands.command()
async def chat(ctx: commands.Context, *tokens: str, attachments: commands.Greedy[discord.Attachment]) -> None:
    # if int(os.environ["OWNER_ID"]) != ctx.author.id:
    #     await ctx.reply("Sorry, this command is temporary unavailable.", mention_author=False)
    #     return
    
    text = " ".join(tokens)
    
    await ctx.typing()
    
    try:
        answer = chatbot_answer(text, ctx.author.id, attachments)

        await ctx.reply(answer)
    except:
        await ctx.reply("Something went wrong")