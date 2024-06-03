# utils.py
import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF

def extract_text_from_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf_data):
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")
    return text

def extract_text_from_file(file_data, file_type):
    if file_type == 'image':
        return extract_text_from_image(file_data)
    elif file_type == 'pdf':
        return extract_text_from_pdf(file_data)
    else:
        return ""
