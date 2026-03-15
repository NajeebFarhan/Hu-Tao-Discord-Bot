import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
BOT_PREFIX = os.environ["BOT_PREFIX"]

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)


@bot.event
async def on_ready() -> None:
    print("Successfully setup")

@bot.event
async def on_connect() -> None:
    print("Connected to Discord")
    

from commands.ping import ping
from commands.chat import chat
from commands.delete_msg import deletemsg
# from commands.help import help

bot.add_command(ping)
bot.add_command(chat)
bot.add_command(deletemsg)
# bot.add_command(help)

 
if __name__ == "__main__":
    bot.run(BOT_TOKEN, log_handler=handler)