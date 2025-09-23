import hikari

from llm import llm_answer

from dotenv import load_dotenv
import os

load_dotenv()

bot = hikari.GatewayBot(intents=hikari.Intents.ALL, token=os.environ["BOT_TOKEN"])
PREFIX = "hu!"


@bot.listen()
async def something(event: hikari.MessageCreateEvent) -> None:
    if not event.is_human:
        return
    
    if not event.content or not event.content.startswith(PREFIX):
        return
    
    
    content = event.content[len(PREFIX):].strip()
    command = content.split(" ")[0]
    message = " ".join(content.split(" ")[1:])
    
    await event.app.rest.trigger_typing(event.channel_id)
    
    match command:
        case "ping":
            print(event.author_id, event.message_id)
            await event.message.respond("Pong")
    
        case "chat":
            answer = llm_answer(message)
            await event.message.respond(answer)
        
bot.run()