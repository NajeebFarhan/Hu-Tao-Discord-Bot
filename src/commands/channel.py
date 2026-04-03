from discord.ext import commands
from libs.chat_channel import ChatChannel

chat_channel = ChatChannel()

@commands.command()
@commands.is_owner()
async def channel(ctx: commands.Context, command: str, channel_name: str):
    
    pass


@commands.command()
@commands.is_owner()
async def deletechannel(ctx: commands.Context):
    
    pass