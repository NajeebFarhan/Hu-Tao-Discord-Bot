from discord.ext import commands
from agent.model import show_history


def truncate(text: str, limit: int = 60) -> str:
    if len(text) > limit:
        return text[:limit] + "..."
    return text


@commands.command()
async def history(ctx: commands.Context, limit: int = 10):
    chat_history = show_history(ctx.author.id)
    print(chat_history)
    await ctx.reply("History command")