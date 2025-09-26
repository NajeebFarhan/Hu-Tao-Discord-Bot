import hikari

from llm import llm_answer
from db import SessionLocal, Chat

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
            human_chat = Chat(
                        message=message,
                        user_id=str(event.author_id),
                        role="human",
                        message_id=str(event.message_id),
                        channel_id=str(event.channel_id)
                    )
            
            answer = llm_answer(message)
            
            res = await event.message.respond(answer)
            
            ai_chat = Chat(
                message=answer,
                user_id=str(res.author.id),
                role="ai",
                message_id=str(res.id),
                channel_id=str(res.channel_id)
            )
            
            try: 
                # TODO: FIX DB ISSUE
                # pass
                with SessionLocal() as session:
                    session.add(human_chat)
                    session.add(ai_chat)
                    session.commit()
                    
                    # data = session.query(Chat).all()
                
                    
            except:
                pass
        
bot.run()