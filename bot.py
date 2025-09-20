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
    
    if not event.content or not event.content.startswith("hu!"):
        return
    
    content = event.content[3:].strip()
    command = content.split(" ")[0]
    message = " ".join(content.split(" ")[1:])
    
    match command:
        case "ping":
            await event.message.respond("Pong")
    
        case "chat":
            answer = llm_answer(message)
            await event.message.respond(answer)

        
bot.run()