from langchain.agents import create_agent
from langchain_ollama.chat_models import ChatOllama
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from dotenv import load_dotenv
from agent.tools import TOOLS
from agent.libs.context_schema import Context


load_dotenv()


conn = sqlite3.connect("memory/agent_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)


model = ChatOllama(model="ministral-3:8b", num_predict=2_000)


agent = create_agent(
    model=model,
    
    tools=TOOLS,
    system_prompt="Your name is Hu Tao. You are a helpful Discord bot. Keep you response under 2000 characters",
    checkpointer=checkpointer,
    context_schema=Context,
)