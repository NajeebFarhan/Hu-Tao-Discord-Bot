from agent.model import checkpointer

def clear_chat(user_id: int) -> None:
    try:
        checkpointer.delete_thread(str(user_id))

    except:
        raise Exception