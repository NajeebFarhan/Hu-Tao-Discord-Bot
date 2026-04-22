from discord.ext import commands

@commands.command()
@commands.is_owner()
async def test(ctx: commands.Context):
    pass

