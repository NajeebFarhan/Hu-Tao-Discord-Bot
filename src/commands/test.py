from discord.ext import commands
from agent.libs.clear_chat import clear_n_chat


@commands.command()
@commands.is_owner()
async def test(ctx: commands.Context, thread_id: int, n: int):
    pass