# utils.py
from PIL import Image
from io import BytesIO
import requests
from base64 import b64encode

def resize_image(image_url, width, height):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    output_buffer = BytesIO()
    resized_image.save(output_buffer, format='JPEG')  # или другой формат
    resized_image_data = output_buffer.getvalue()
    
    return f"data:image/jpeg;base64,{b64encode(resized_image_data).decode('utf-8')}"
