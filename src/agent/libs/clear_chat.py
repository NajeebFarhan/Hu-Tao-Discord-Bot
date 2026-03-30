from agent.model import agent, checkpointer
from langchain.messages import HumanMessage

def clear_chat(user_id: int) -> None:
    try:
        checkpointer.delete_thread(str(user_id))

    except:
        raise Exception
    
# def clear_n_chat(user_id: int, n: int = 1) -> bool:
#     config = {"configurable": {"thread_id": user_id}}

#     state = agent.get_state(config) 

#     if not state:
#         return False

#     messages = state.values.get("messages", [])

#     # find indices of all human messages
#     human_indices = [
#         i for i, m in enumerate(messages)
#         if isinstance(m, HumanMessage)
#     ]

#     if not human_indices:
#         return False

#     # determine where to cut history
#     if len(human_indices) <= n:
#         new_messages = []
#     else:
#         cutoff_index = human_indices[-n]
#         new_messages = messages[:cutoff_index]

#     # overwrite state
#     agent.update_state(
#         config,
#         {"messages": new_messages}
#     )

#     return True