# utils.py
import pytesseract
from PIL import Image
import io

def extract_text_from_image(image_data):
    # Convert the in-memory image data to a PIL image
    image = Image.open(io.BytesIO(image_data))
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(image)
    return text
