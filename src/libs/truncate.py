def truncate(text: str, limit: int, remove_format: bool=True):
    if remove_format:
        text = text.replace("\n", " ")
    return text[:limit] + ("..." if len(text) > limit else "")