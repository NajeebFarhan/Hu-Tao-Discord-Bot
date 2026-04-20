import textwrap

def smart_chunk(text, size=1900):
    return textwrap.wrap(text, width=size, replace_whitespace=False)