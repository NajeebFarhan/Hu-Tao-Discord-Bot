from langchain.agents import create_agent
from langchain_ollama.chat_models import ChatOllama
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import os
from dotenv import load_dotenv
from agent.tools import TOOLS
from agent.libs.context_schema import Context


load_dotenv()


conn = sqlite3.connect("memory/agent_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)


model = ChatOllama(
    model="ministral-3:8b",
    num_predict=1800,
    temperature=0,
    keep_alive=os.getenv("OLLAMA_KEEP_ALIVE", "30m"),
)

tool_names = ", ".join(tool.name for tool in TOOLS)

SYSTEM_PROMPT = (
    "Your name is Hu Tao. You are a helpful Discord bot. Keep your response under 1800 characters. "
    f"You can only use these tools: {tool_names}. "
    "Never call a tool that is not in this list. "
    "If no listed tool is needed, answer directly without using any tool."
)


agent = create_agent(
    model=model,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
    context_schema=Context,
)