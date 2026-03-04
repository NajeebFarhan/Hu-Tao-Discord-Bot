from discord.ext import commands

@commands.command()
async def ping(ctx: commands.Context) -> None:
    await ctx.reply("Pong", mention_author=False)