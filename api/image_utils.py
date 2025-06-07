import base64
import pytesseract
from PIL import Image
from io import BytesIO

def extract_text_from_base64(base64_str: str) -> str:
    try:
        image_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(image_data))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error decoding image: {str(e)}"
