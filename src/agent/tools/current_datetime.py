from langchain.tools import tool

@tool
def current_datetime_tool() -> str:
    """
    Returns the current system date and time.
    Useful when the LLM needs to know the current time.
    """
    from datetime import datetime

    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")