def truncate(text: str, limit: int):
    text = text.replace("\n", " ")
    return text[:limit] + ("..." if len(text) > limit else "")