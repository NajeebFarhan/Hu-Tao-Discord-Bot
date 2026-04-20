from agent.model import agent, checkpointer
from langchain.messages import HumanMessage, RemoveMessage

def clear_chat(thread_id: int) -> None:
    try:
        checkpointer.delete_thread(str(thread_id))

    except:
        raise Exception
    
def clear_n_chat(thread_id: int, n: int):
    config = {"configurable": {"thread_id": thread_id}}

    snapshot = agent.get_state(config) # type:ignore
    state = snapshot.values

    messages = state["messages"]

    # # # find indices of all human messages
    human_indices = [
        i for i, m in enumerate(messages)
        if isinstance(m, HumanMessage)
    ]
    print(human_indices)

    if not human_indices:
        return False

    # # # determine where to cut history
    if len(human_indices) <= n:
        clear_chat(thread_id)
        return True
    
    to_remove = messages[human_indices[-n]:]

    removal_updates = [
        RemoveMessage(id=m.id)
        for m in to_remove
    ]

    agent.update_state(config, {"messages": removal_updates}) # type:ignore

    return True