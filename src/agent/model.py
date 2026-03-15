from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_ollama.chat_models import ChatOllama
from langchain.messages import HumanMessage, AIMessage, SystemMessage
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
import discord
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Any

load_dotenv()


search = TavilySearchResults()


@tool
def get_current_datetime() -> str:
    """
    Returns the current system date and time.
    Useful when the LLM needs to know the current time.
    """
    from datetime import datetime

    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


# @tool
# def analyze_image(prompt: str, runtime: ToolRuntime[Context]) -> str:
#     """
#     Analyze an image stored in runtime context.
#     The user prompt describes what to do with the image.
#     If no image is provided, inform the user about it.
#     """

#     images_urls = [
#         attachment.url
#         for attachment in runtime.context.attachments
#         if attachment.filename.endswith(("jpg", "jpeg", "png"))
#     ]
    
#     if not images_urls:
#         return "No images are found"
    
    


tools = [get_current_datetime, search]


conn = sqlite3.connect("memory/agent_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)


@dataclass
class Context:
    user_id: int
    attachments: list[discord.Attachment]


model = ChatOllama(model="llama3.2:3b")

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="You are a helpful Discord bot that can use tools. Keep you response under 100 words",
    checkpointer=checkpointer,
    context_schema=Context,
)


def chatbot_answer(prompt: str, user_id: int, attachments) -> str:
    config = {"configurable": {"thread_id": user_id}}

    result = agent.invoke(
        {"messages": [HumanMessage(prompt)]},
        config=config,  # type:ignore
        context=Context(user_id, attachments),
    )

    content = result["messages"][-1].content

    return content


# print(result["messages"][-1].content)
