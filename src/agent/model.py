from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_ollama.chat_models import ChatOllama
from langchain.messages import HumanMessage, AIMessage, SystemMessage
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv

load_dotenv()


model = ChatOllama(model="qwen3:4b")


search = TavilySearchResults()

tools = [search]


conn = sqlite3.connect("memory/agent_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)


agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="You are a helpful Discord bot that can use tools. Keep you response under 100 words",
    checkpointer=checkpointer,
)


def chatbot_answer(prompt: str, user_id: int) -> str:
    config = {"configurable": {"thread_id": user_id}}

    result = agent.invoke(
        {"messages": [HumanMessage(prompt)]}, 
        config=config # type:ignore
    )
    
    content = result["messages"][-1].content
    
    return content

# print(result["messages"][-1].content)
