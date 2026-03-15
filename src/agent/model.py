from langchain.agents import create_agent
from langchain_ollama.chat_models import ChatOllama
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver

# from agent.tools import get_current_datetime, get_search_result
from .tools import search_result_tool, current_datetime_tool
 
import sqlite3

import discord

from dataclasses import dataclass








# @tool
# def analyze_image(prompt: str, runtime: ToolRuntime[Context]) -> str:
#     """
#     Analyze an image stored in runtime context.
#     The user prompt describes what to do with the image.
#     If no image is provided, inform the user about it.
#     """

#     images_urls = [
#         attachment.url
#         for attachment in runtime.context.attachments
#         if attachment.filename.endswith(("jpg", "jpeg", "png"))
#     ]
    
#     if not images_urls:
#         return "No images are found"
    
    


tools = [search_result_tool, current_datetime_tool]


conn = sqlite3.connect("memory/agent_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)


@dataclass
class Context:
    user_id: int
    attachments: list[discord.Attachment]


model = ChatOllama(model="llama3.2:3b")

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="You are a helpful Discord bot that can use tools. Keep you response under 100 words",
    checkpointer=checkpointer,
    context_schema=Context,
)


def chatbot_answer(prompt: str, user_id: int, attachments) -> str:
    config = {"configurable": {"thread_id": user_id}}

    result = agent.invoke(
        {"messages": [HumanMessage(prompt)]},
        config=config,  # type:ignore
        context=Context(user_id, attachments),
    )

    content = result["messages"][-1].content

    return content

















# import os

# img = os.path.join(os.path.abspath('.'), "src\\agent\\adorable-baby-panda-cub-eating-bamboo-on-a-tree-branch-in-a-lush-green-forest-habitat-photo.jpeg")

# import base64

# def image_to_data_url(path):
#     with open(path, "rb") as f:
#         encoded = base64.b64encode(f.read()).decode()
#     return f"data:image/jpeg;base64,{encoded}"

# image = image_to_data_url(img)

# message = HumanMessage(
#     content=[
#         {"type": "text", "text": "What is in this image?"},
#         {
#             "type": "image_url",
#             "image_url": image
#         }
#     ]
# )

# # response = ollama.chat(
# #     model="qwen3-vl:2b",
# #     messages=[
# #         {
# #             "role": "user",
# #             "content": "Describe this image",
# #             "images": [img]
# #         }
# #     ]
# # )

# # print(response["message"]["content"])

# print(model.invoke([message]))

# # print(result["messages"][-1].content)
