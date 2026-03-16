from langchain.agents import create_agent
from langchain_ollama.chat_models import ChatOllama
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.tools import tool, ToolRuntime

# from agent.tools import get_current_datetime, get_search_result
# from tools import current_datetime_tool, analyze_images_tool #, search_result_tool
 
import sqlite3

import discord

from dataclasses import dataclass  
from dotenv import load_dotenv
load_dotenv()  



@tool
def current_datetime_tool() -> str:
    """
    Returns the current system date and time.
    Useful when the LLM needs to know the current time.
    """
    from datetime import datetime

    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")




tools = [current_datetime_tool] #, analyze_images_tool, search_result_tool]


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
    # checkpointer=checkpointer,
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

# if __name__ == "__main__":
    
#     agent.invoke(
#         {
#             "messages": [
#                 HumanMessage("how are you doing?")
#             ]
#         },
#         config={"configurable": {"thread_id": 1}}
#     )