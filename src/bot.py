import discord
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
BOT_PREFIX = os.environ["BOT_PREFIX"]

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
    
    text = " ".join(contexts[1:])
    # print(contexts)
    # user = await client.fetch_user(message.author.id)
    
    # dm = await user.create_dm()
    
    # await dm.send("Hello")
    await message.reply("hello")
    
    

 
if __name__ == "__main__":
    client.run(BOT_TOKEN)