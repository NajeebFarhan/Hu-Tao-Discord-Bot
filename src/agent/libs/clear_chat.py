from agent.model import agent, checkpointer
from langchain.messages import HumanMessage

def clear_chat(thread_id: int) -> None:
    try:
        checkpointer.delete_thread(str(thread_id))

    except:
        raise Exception
    
# def clear_n_chat(thread_id: int, n: int) -> bool:
#     config = {"configurable": {"thread_id": thread_id}}
    
#     saver = checkpointer.get(config) 

#     if not saver:
#         return False
    
#     messages = saver["channel_values"].get("messages", [])
    
#     for m in messages:
#         m.pretty_print()    


    # # find indices of all human messages
    # human_indices = [
    #     i for i, m in enumerate(messages)
    #     if isinstance(m, HumanMessage)
    # ]
    # print(human_indices)

    # if not human_indices:
    #     return False

    # # determine where to cut history
    # if len(human_indices) <= n:
    #     new_messages = []
    # else:
    #     cutoff_index = human_indices[-n]
    #     new_messages = messages[:cutoff_index]

    # # overwrite state
    # checkpointer.put(
    #     config=config,
    #     checkpoint=state,
    #     metadata={},
    #     new_versions=
    # )

    # return True