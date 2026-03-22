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
    

from commands import COMMANDS

for cmm in COMMANDS:
    bot.add_command(cmm)

 
if __name__ == "__main__":
    bot.run(BOT_TOKEN, log_handler=handler)