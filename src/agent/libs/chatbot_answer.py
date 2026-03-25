from agent.model import agent
from langchain.messages import HumanMessage
from agent.libs.image_data import image_url_to_data_url
from agent.libs.context_schema import Context
from discord import Attachment
from discord.ext.commands import Greedy

def chatbot_answer(prompt: str, user_id: int, attachments: Greedy[Attachment]) -> str:
    config = {"configurable": {"thread_id": user_id}}

    content: list = [
        {"type": "text", "text": prompt},
    ]

    for attachment in attachments:
        content.append({"type": "image_url", "image_url": image_url_to_data_url(attachment.url)})

    result = agent.invoke(
        {"messages": [HumanMessage(content=content)]},
        config=config,  # type:ignore
        context=Context(user_id, prompt, attachments),
    )

    answer = result["messages"][-1].content

    return answer