from langchain.tools import tool, ToolRuntime
import ollama
import discord
from dataclasses import dataclass
import base64
import requests
from agent.libs.context_schema import Context
    
    
def image_url_to_data_url(image_url: str):
    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    return base64.b64encode(response.content).decode()


@tool
def analyze_images_tool(runtime: ToolRuntime[Context]) -> str:
    """
    Use this tool to see and analyze image(s) that the user provided you from discord.
    The user provides prompt telling what to do with the image(s).
    
    This tool will return descriptive text about the image, send this as the output to the user.
    """
    print("analyze image tool called!")
    images_urls = [
        attachment.url
        for attachment in runtime.context.attachments
    ]
    
    if not images_urls:
        return "You did not provide any images."
    
    imgs = [image_url_to_data_url(url) for url in images_urls]    
    
    try:
        response = ollama.chat(
            model="qwen3-vl:2b",
            messages=[
                {
                    "role": "user",
                    "content": runtime.context.prompt,
                    "images": imgs
                }
            ]
        )
        
        description = response["message"]["content"]
        
        # print(runtime.context.prompt)
        # print(images_urls)
        # print(description)
        
        return description
    
    except:
        return "Something went wrong with the image analysis."