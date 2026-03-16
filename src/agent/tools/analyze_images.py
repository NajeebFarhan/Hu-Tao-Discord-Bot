from langchain.tools import tool, ToolRuntime
import ollama
import discord
from dataclasses import dataclass
import base64
import requests
import tempfile
import os



@dataclass
class Context:
    user_id: int
    attachments: list[discord.Attachment]
    
    
def image_url_to_data_url(image_url: str) -> str:
    """
    Download an image from a URL, convert it to a base64 data URL,
    then delete the temporary file.
    """

    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "image/jpeg")

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        for chunk in response.iter_content(8192):
            temp_file.write(chunk)

        temp_path = temp_file.name

    try:
        with open(temp_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        return f"data:{content_type};base64,{encoded}"

    finally:
        os.remove(temp_path)


@tool
def analyze_images_tool(prompt: str, runtime: ToolRuntime[Context]) -> str | list[str]:
    """
    Analyze image(s) stored in runtime context.
    The user prompt describes what to do with the image(s).
    If no image is provided, inform the user about it.
    
    May return a single string or a list of string.
    """

    images_urls = [
        attachment.url
        for attachment in runtime.context.attachments
        if attachment.filename.endswith(("jpg", "jpeg", "png"))
    ]
    imgs = []
    
    if not images_urls:
        return "No images are found"
    
    
    imgs = [image_url_to_data_url(url) for url in images_urls]
    
    
    response = ollama.chat(
        model="qwen3-vl:2b",
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [imgs]
            }
        ]
    )
    
    return response["message"]["content"]
    
    
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