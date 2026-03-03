import discord
import logging
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
BOT_PREFIX = os.environ["BOT_PREFIX"]

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)

@client.event
async def on_ready() -> None:
    print("Successfully setup")

@client.event
async def on_connect() -> None:
    print("Connected to Discord")

@client.event
async def on_message(message: discord.message.Message) -> None:
    if message.author == client.user:
        return
    
    if not message.content.startswith(BOT_PREFIX):
        return
    
    content = message.content[len(BOT_PREFIX):]
    
    if not content:
        return
    
    contexts = content.split(" ")
    
    command = contexts[0]
 
    
    

 
if __name__ == "__main__":
    client.run(BOT_TOKEN, log_handler=handler)