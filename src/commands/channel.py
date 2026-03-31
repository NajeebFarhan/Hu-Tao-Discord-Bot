from discord.ext import commands
import sqlite3

@commands.command()
@commands.is_owner()
async def channel(ctx: commands.Context, command: str, channel_name: str):
    
    pass


@commands.command()
@commands.is_owner()
async def deletechannel(ctx: commands.Context):
    
    pass