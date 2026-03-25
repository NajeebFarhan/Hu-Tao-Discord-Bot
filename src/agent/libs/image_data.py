import base64
import requests
from io import BytesIO
from PIL import Image

def image_url_to_data_url(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()

    # load image regardless of format (including AVIF)
    image = Image.open(BytesIO(response.content)).convert("RGB")

    # convert to PNG in memory
    buffer = BytesIO()
    image.save(buffer, format="PNG")

    encoded = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{encoded}"