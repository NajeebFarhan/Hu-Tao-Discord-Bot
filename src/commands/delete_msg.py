from discord.ext import commands
from agent.libs.clear_chat import clear_chat, clear_n_chat
import os


@commands.command()
async def deletechat(ctx: commands.Context, n: int | None = None) -> None:
    bot: commands.Bot = ctx.bot
    
    if n and n <= 0:
        await ctx.reply(f"Sorry, it's nto possible to delete{n} messages", mention_author=False)
        return
    
    if n:
        warning = f"**Are you sure you want to delete your last {'message' if n == 1 else f'{n} messages'} from the chat history? To confirm:**\n"
    else:
        warning = "**Are you sure you want to delete your entire chat history? To confirm:**\n"
        
    confirmation_msg_ref = await ctx.reply(
            f"{warning}"
            "# Reply `yes` to this message\n"
            "-# (note: reply this message, sending plain message witout replying will not do anything)"
        )
    
    def check(m):
        return (
            m.reference
            and m.reference.message_id == confirmation_msg_ref.id
            and m.author == ctx.author
        )

    try:
        user_reply = await bot.wait_for("message", check=check, timeout=10)

        if user_reply.content == "yes":
            try:
                if not n:
                    clear_chat(ctx.author.id)
                    await ctx.reply("Your chat history has been deleted")    
                elif n > 0: 
                    clear_n_chat(ctx.author.id, n)
                    await ctx.reply(f"Your last {n if n > 1 else ''} {'messages have' if n > 1 else 'message has'} been deleted")
        
            except:
                await ctx.reply("Something went wrong. Your chat history is not deleted")
        else:
            await ctx.reply("Incorrect response. This action has been aborted")
            
    except:
        await ctx.reply("Timeout! Your chat history is not deleted")


@commands.command()
@commands.is_owner()
async def deleteall(ctx: commands.Context) -> None:
    bot: commands.Bot = ctx.bot

    DANGER_TEXT = "I am about to nuke the whole chat history of all users and I will take the full responsibility for anyone's lost relationship with my bot."

    danger_ref = await ctx.reply(
        f"Type the text below to confirm nuking the entire chat database: \n{DANGER_TEXT}"
    )


    def check(m):
        return (
            m.reference
            and m.reference.message_id == danger_ref.id
            and m.author == ctx.author
        )

    try:
        owner_reply = await bot.wait_for("message", check=check, timeout=30)

        if owner_reply.content == DANGER_TEXT:
            os.remove("memory/agent_memory.db")
            await ctx.reply("The whole database has been nuked")
        else:
            await ctx.reply("Ehh! Wrong text, the database is not deleted and the chats are still safe")
            
    except:
        await ctx.reply("Timeout! The database is not deleted and all the chats are still safe")
