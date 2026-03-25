from langchain.agents import create_agent
from langchain_ollama.chat_models import ChatOllama
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.tools import tool, ToolRuntime
import sqlite3
from dotenv import load_dotenv
from agent.tools import TOOLS
from agent.libs.context_schema import Context
from typing import Any
from discord import Attachment
from discord.ext.commands import Greedy


load_dotenv()


conn = sqlite3.connect("memory/agent_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)


model = ChatOllama(model="ministral-3:8b")


agent = create_agent(
    model=model,
    tools=TOOLS,
    system_prompt="Your name is Hu Tao. You are a helpful Discord bot. Keep you response under 100 words",
    checkpointer=checkpointer,
    context_schema=Context,
)


import base64
import requests
from io import BytesIO
from PIL import Image


def image_url_to_data_url(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()

    # load image regardless of format (including AVIF)
    image = Image.open(BytesIO(response.content)).convert("RGB")

    # convert to PNG in memory
    buffer = BytesIO()
    image.save(buffer, format="PNG")

    encoded = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{encoded}"


def chatbot_answer(prompt: str, user_id: int, attachments: Greedy[Attachment]) -> str:
    config = {"configurable": {"thread_id": user_id}}

    content: list = [
        {"type": "text", "text": prompt},
    ]

    for attachment in attachments:
        content.append({"type": "image_url", "image_url": image_url_to_data_url(attachment.url)})

    result = agent.invoke(
        {"messages": [HumanMessage(content=content)]},
        config=config,  # type:ignore
        context=Context(user_id, prompt, attachments),
    )

    answer = result["messages"][-1].content

    return answer


def clear_chat(user_id: int) -> None:
    try:
        checkpointer.delete_thread(str(user_id))

    except:
        raise Exception


def show_history(user_id: int) -> None:
    config = {"configurable": {"thread_id": user_id}}

    chat_history = checkpointer.get(config)  # type:ignore

    print(chat_history)
