from agent.model import checkpointer
from langchain.messages import HumanMessage, AIMessage

def show_history(user_id: int) -> list[HumanMessage | AIMessage]:
    chat_history = checkpointer.get({"configurable": {"thread_id": user_id}})
    
    if chat_history:
        chat_history = chat_history["channel_values"]["messages"]
    else:
        chat_history = []

    return chat_history
