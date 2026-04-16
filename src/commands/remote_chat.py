from discord.ext import commands
import discord

last_channel_id: int | None = None

@commands.command(aliases=["rc"])
@commands.is_owner()
async def remote_chat(ctx: commands.Context, channel_id: int, *token: str, attachments: commands.Greedy[discord.Attachment]):
    bot: commands.Bot = ctx.bot
    
    channel = bot.get_channel(channel_id)
    message = " ".join(token)
    
    for attachment in attachments:
        message += "\n" + attachment.url
 
    if channel:
        try:
            await channel.send(message) # type:ignore
            
        except:
            print("not send")
            
            
@commands.command(aliases=["rp"])
@commands.is_owner()
async def remote_reply(ctx: commands.Context, channel_id: int, message_id: int, *token: str, attachments: commands.Greedy[discord.Attachment]):
    bot: commands.Bot = ctx.bot
    
    channel = bot.get_channel(channel_id)
    if channel:
        message = await channel.fetch_message(message_id) # type:ignore
    else:
        return 
    
    reply = " ".join(token)
    
    for attachment in attachments:
        reply += "\n" + attachment.url
    # if guild:
    #     channel = guild.get_channel(channel_id)
        
    if message:
        try:
            await message.reply(reply, mention_author=False)
            
        except:
            print("not replied")
      
            
@commands.command(aliases=["re"])
@commands.is_owner()
async def remote_edit(ctx: commands.Context, channel_id: int, message_id: int, *token: str):
    bot: commands.Bot = ctx.bot
    
    channel = bot.get_channel(channel_id)
    if channel:
        message = await channel.fetch_message(message_id) # type:ignore
    else:
        return 
    
    edited_message = " ".join(token)
    # edited_message = message
    
    if message:
        try:
            await message.edit(content=edited_message)
            
        except:
            print("not edited")
            
            
@commands.hybrid_command(aliases=["rd"])
@commands.is_owner()
async def remote_delete(ctx: commands.Context, message_id: int, channel_id: int | None):
    bot: commands.Bot = ctx.bot
    
    if channel_id:
        channel = bot.get_channel(channel_id)
    else:
        channel = ctx.channel
        
    if channel:
        message = await channel.fetch_message(message_id) # type:ignore
    else:
        return 
    
    await message.delete()
    

@commands.hybrid_command(aliases=["rpin"])
@commands.is_owner()
async def remote_pin(ctx: commands.Context, message_id: int, channel_id: int | None, pin: bool):
    
    bot: commands.Bot = ctx.bot
    
    if channel_id:
        channel = bot.get_channel(channel_id)
    else:
        channel = ctx.channel
        
    if channel:
        message = await channel.fetch_message(message_id) # type:ignore
    else:
        return 
    
    if pin:
        await message.pin()
    else:
        await message.unpin()
        

@commands.hybrid_command(aliases=["rr"])
@commands.is_owner()
async def remote_reaction(ctx: commands.Context, message_id: int, emoji: str, channel_id: int | None):
    
    bot: commands.Bot = ctx.bot
    
    if channel_id:
        channel = bot.get_channel(channel_id)
    else:
        channel = ctx.channel
        
    if channel:
        message = await channel.fetch_message(message_id) # type:ignore
    else:
        return 
    
    if message:
        await message.add_reaction(emoji)
        
    # channel.create_forum()
    
# @commands.hybrid_command(aliases=["nick"])
# @commands.is_owner()
# async def change_nick(ctx: commands.Context, user_id: int, channel_id: int | None, nick: str):
    
    
#     member = await ctx.guild.fetch_member(user_id)
    
#     old_name = member.display_name
    
#     # try:
#     if ctx.bot_permissions.all():
#         await member.edit(nick=nick)

#         await ctx.send(f"{old_name} has been renamed to {nick}")
#     else:
#         print("something went wrong")
    