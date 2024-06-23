# utils.py
import pytesseract
from PIL import Image
import io
import cv2
import fitz  # PyMuPDF
import pandas as pd
# def extract_text_from_image(image_data):
#     image = Image.open(io.BytesIO(image_data))
#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     # Apply binarization
#     _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     # Remove noise
#     denoised = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)
#     text = pytesseract.image_to_string(denoised)
#     return text
#
# def extract_text_from_pdf(pdf_data):
#     pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
#     text = ""
#     for page_num in range(len(pdf_document)):
#         page = pdf_document.load_page(page_num)
#         text += page.get_text("text")
#     return text
# # Information Retrieve Button(New Feature)
# def information_retrieve(text):
#     columns = ['Item ID', 'Document Owner', 'Type', 'Date', 'Supplier', 'Purchase Order Number', 'Document Reference', 'Due Date', 'Category', 'Customer', 'Description', 'Currency', 'Total Amount', 'Tax', 'Tax Amount', 'Net Amount']
#     data = []  # Collect data as a list of dictionaries
#
#     # Assume you have some logic here to extract information from text and append to data
#     # Example of appending a row (replace with actual logic)
#     data.append({
#         'Item ID': '12345',
#         'Document Owner': 'John Doe',
#         'Type': 'Invoice',
#         'Date': '2023-06-01',
#         'Supplier': 'ABC Corp',
#         'Purchase Order Number': 'PO123456',
#         'Document Reference': 'INV123456',
#         'Due Date': '2023-06-15',
#         'Category': 'Office Supplies',
#         'Customer': 'XYZ Ltd',
#         'Description': 'Office chairs',
#         'Currency': 'USD',
#         'Total Amount': 1500,
#         'Tax': '10%',
#         'Tax Amount': 150,
#         'Net Amount': 1350
#     })
#
#     # Convert list of dictionaries to DataFrame
#     df = pd.DataFrame(data, columns=columns)
#     return df
#
# def extract_text_from_file(file_data, file_type):
#     if file_type == 'image':
#         return extract_text_from_image(file_data)
#     elif file_type == 'pdf':
#         return extract_text_from_pdf(file_data)
#     else:
#         return ""
import io
from PIL import Image
import cv2
import pytesseract
import fitz  # PyMuPDF
import pandas as pd
import numpy as np


def extract_text_from_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    denoised = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)
    text = pytesseract.image_to_string(denoised)
    return text


def extract_text_from_pdf(pdf_data):
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")
    return text


def information_retrieve(text):
    columns = ['Item ID', 'Document Owner', 'Type', 'Date', 'Supplier', 'Purchase Order Number', 'Document Reference',
               'Due Date', 'Category', 'Customer', 'Description', 'Currency', 'Total Amount', 'Tax', 'Tax Amount',
               'Net Amount']
    data = []  # Collect data as a list of dictionaries

    # Assume you have some logic here to extract information from text and append to data
    # Example of appending a row (replace with actual logic)
    data.append({
        'Item ID': '12345',
        'Document Owner': 'John Doe',
        'Type': 'Invoice',
        'Date': '2023-06-01',
        'Supplier': 'ABC Corp',
        'Purchase Order Number': 'PO123456',
        'Document Reference': 'INV123456',
        'Due Date': '2023-06-15',
        'Category': 'Office Supplies',
        'Customer': 'XYZ Ltd',
        'Description': 'Office chairs',
        'Currency': 'USD',
        'Total Amount': 1500,
        'Tax': '10%',
        'Tax Amount': 150,
        'Net Amount': 1350
    })

    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data, columns=columns)
    return df


def extract_text_from_file(file_data, file_type):
    if file_type == 'image':
        return extract_text_from_image(file_data)
    elif file_type == 'pdf':
        return extract_text_from_pdf(file_data)
    else:
        return ""



