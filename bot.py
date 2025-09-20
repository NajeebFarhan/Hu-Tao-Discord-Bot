import hikari

from llm import llm_answer

from dotenv import load_dotenv
import os

load_dotenv()

bot = hikari.GatewayBot(intents=hikari.Intents.ALL, token=os.environ["BOT_TOKEN"])


@bot.listen()
async def something(event: hikari.MessageCreateEvent) -> None:
    if not event.is_human:
        return
    
    if event.content and event.content.startswith("hu!"):
        message = event.content[3:].strip()

        answer = llm_answer(message)
        
        await event.message.respond(answer)

        
bot.run()