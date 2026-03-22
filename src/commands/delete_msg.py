from discord.ext import commands
import discord
import os


@commands.command()
async def deletemsg(ctx: commands.Context) -> None:
    pass


@commands.command()
async def deleteall(ctx: commands.Context) -> None:
    if int(os.environ["OWNER_ID"]) != ctx.author.id:
        await ctx.reply("Stay away from it, hacker!")
        return

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
            await ctx.reply("Ehh! Wrong text, the database is not deleted and the chats are still safe.")
            
    except:
        await ctx.reply("Timeout! The database is not deleted and all the chats are still safe.")
