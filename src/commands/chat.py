import asyncio
from discord.ext import commands
import discord
from agent.libs.chatbot_answer import chatbot_answer
from libs.logger import log_command_error
from libs.carousel import CarouselView
from libs.smart_chunk import smart_chunk


async def get_reference(ctx: commands.Context):
    ref = ctx.message.reference
    message = None
    
    if ref:
        if not ref.fail_if_not_exists:
            return None
            
        if ref.message_id:
            message = await ctx.channel.fetch_message(ref.message_id)
         
    if message:   
        return message
    
    return None
        


@commands.command()
async def chat(ctx: commands.Context, attachments: commands.Greedy[discord.Attachment]) -> None:
    # if int(os.environ["OWNER_ID"]) != ctx.author.id:
    #     await ctx.reply("Sorry, this command is temporary unavailable.", mention_author=False)
    #     return
    
    text = ctx.message.content.removeprefix((ctx.prefix or "") + "chat")
    
    if not text:
        return
    
    ref_message = await get_reference(ctx)
    
    if ref_message:
        if ref_message.content:
            text = f"{text}\n\n{ref_message.content}"
        
        attachments.extend(ref_message.attachments)

    try:
        async with ctx.typing():
            # Run synchronous LLM call in a worker thread so Discord heartbeats stay responsive.
            answer = await asyncio.to_thread(chatbot_answer, text, ctx.author.id, attachments)
            
        message_parts = smart_chunk(answer)

        if len(message_parts) == 1:
            await ctx.reply(message_parts[0], mention_author=False)

        else:
            view = CarouselView(message_parts, ctx.author.id)
            content = f"{message_parts[0]}\n\n-# Page 1/{len(message_parts)}"
            # disable prev initially
            view.prev_button.disabled = True

            await ctx.reply(
                content=content,
                view=view,
                mention_author=False
            )
        
    except Exception as e:
        log_command_error(ctx, e)
        await ctx.reply("Something went wrong", mention_author=False)