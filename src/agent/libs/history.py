from agent.model import checkpointer

def show_history(user_id: int) -> None:
    config = {"configurable": {"thread_id": user_id}}

    chat_history = checkpointer.get(config)  # type:ignore

    print(chat_history)
