from langchain.agents import create_agent
from langchain_ollama.chat_models import ChatOllama
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.tools import tool, ToolRuntime
import sqlite3
from dotenv import load_dotenv
from agent.tools import current_datetime_tool, analyze_images_tool, search_result_tool
from agent.libs.context_schema import Context
from typing import Any
from discord import Attachment
from discord.ext.commands import Greedy

load_dotenv()


# tools = [current_datetime_tool, analyze_images_tool, search_result_tool]
tools = [current_datetime_tool, search_result_tool]


conn = sqlite3.connect("memory/agent_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)


# model = ChatOllama(model="llama3.2:3b")
# model = ChatOllama(model="gemma3:12b")
model = ChatOllama(model="ministral-3:8b")


agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="Your name is Hu Tao. You are a helpful Discord bot. Keep you response under 100 words",
    checkpointer=checkpointer,
    context_schema=Context,
)


def chatbot_answer(prompt: str, user_id: int, attachments: Greedy[Attachment]) -> str:
    config = {"configurable": {"thread_id": user_id}}
    
    content: list[dict[Any, Any]] = [
        {"type": "text", "text": prompt},
    ]
    
    for attachment in attachments:
        content.append({"type": "image", "url": attachment.url})

    result = agent.invoke(
        {"messages": [HumanMessage(content_blocks=content)]}, # type:ignore
        config=config,  # type:ignore
        context=Context(user_id, prompt, attachments),
    )
    print(result)
    answer = result["messages"][-1].content
    print(content)

    # print(result)
    # print(content)

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
