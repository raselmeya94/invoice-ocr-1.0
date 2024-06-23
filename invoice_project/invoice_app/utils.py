#utils.py
import io
import re
from PIL import Image
import cv2
import pytesseract
import fitz  # PyMuPDF
import pandas as pd
import numpy as np
###
# from pdf2image import convert_from_path
# import pytesseract
# import pdfplumber
# import pandas as pd

# def convert_pdf_to_images_zafi(pdf_path):
#     return convert_from_path(pdf_path, dpi=300)

# def ocr_image_zafi(image):
#     return pytesseract.image_to_string(image, lang='eng')

# def extract_text_from_pdf_zafi(pdf_path):
#     images = convert_pdf_to_images_zafi(pdf_path)
#     text = ""
#     for image in images:
#         text += ocr_image_zafi(image) + "\n"
#     return text
##

def extract_text_from_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
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
# def text_to_info_finder(text):
#     # Remove extra spaces
#     invoice_text = ' '.join(text.split())
#     # Replace "ate" with "Date"
#     invoice_text = invoice_text.replace('ate', 'Date')

#     # Normalize punctuation if needed
#     # Example: Replace different types of dashes with a single dash
#     invoice_text = invoice_text.replace('———', '-') 

#     # Remove special characters like '¢', '(', ')'
#     special_chars = ['¢', '(', ')']
#     for char in special_chars:
#         invoice_text = invoice_text.replace(char, '')

#     # Normalize punctuation if needed
#     # Example: Replace different types of dashes with a single dash
#     invoice_text = invoice_text.replace('———', '-') 
    
#     # Define regex patterns for extracting specific columns
    # patterns = {
    #     'VAT Reg No': r"(?: V\.A\.T\. Reg\. No\.|Registration\:|VAT Reg No|VAT No\.:)\s*(GB \d{3} \d{3} \d{3}|GB \d{3} \d{4} \d{2}|(GB\d{9}))", 
    #     'Company Reg No': r"Company Reg No\. (\w+)",
    #     'Invoice No': r"(?:InvoiceNo|invoiceNo|Invoice No|Invoice \#)\s*—*\s*([A-Za-z0-9]+)|INV\d{6}|d{9}",
    #     'Date': r"(?:Date|Date:|ate) (\d{2}/\d{2}/\d{4})|\d{2}/\d{2}/\d{4}",
    #     # 'Supplier':
    #     'Goods Total': r"GOODS TOTAL (\d+\.\d+)",
    #     'VAT Total': r"VAT TOTAL (\d+\.\d+)",
    #     'Invoice Total': r"INVOICE TOTAL (\d+\.\d+)"
    # }
#     pattern = re.compile(r'(?P<key>Account Number|Payment Date|Page|Payment Reference)\s*(?P<value>\d+/\d+/\d+|\d+|[A-Za-z0-9]+)')
    
#     # Find all matches
#     matches = pattern.findall(text)
    
#     # Create a dictionary from the matches
#     extracted_values = {key: value for key, value in matches}

#     # Initialize an empty dictionary to store extracted values
#     extracted_values = {}
    

#     # Iterate through patterns and extract values using regex
#     for key, pattern in patterns.items():
#         match = re.search(pattern, invoice_text)
#         if match:
#             extracted_values[key] = match.group(1)
#         else:
#             extracted_values[key] = None
#     print(extracted_values)
#     # Create DataFrame from extracted values
#     invoice_df = pd.DataFrame([extracted_values])
#     return invoice_df
def text_to_info_finder(text):
    # Normalize the text by removing extra spaces and replacing known issues
    text = ' '.join(text.split())
    text = text.replace('ate', 'Date')
    
    # Remove special characters
    special_chars = ['¢', '(', ')']
    for char in special_chars:
        text = text.replace(char, '')

    # Define regex patterns for extracting specific columns
    patterns = {
    'VAT Reg No': r"(?: V\.A\.T\. Reg\. No\.|Registration\:|VAT Reg No|VAT No\.:)\s*(GB \d{3} \d{3} \d{3}|GB \d{3} \d{4} \d{2}|(GB\d{9}))", 
    'Company Reg No': r"Company Reg No\. (\w+)",
    'Invoice No': r"(?:InvoiceNo|invoiceNo|Invoice No|Invoice Number|Invoice \#)\s*([A-Za-z0-9]+)|INV\d{6}|d{9}|\bINV\d{6}\b",
    'Date': r"(?:Date|Date:|ate) (\d{2}/\d{2}/\d{4})|\d{2}/\d{2}/\d{4}",
    'Payment Due':r"Payment Due:\s*\n?\s*(\d{2}/\d{2}/\d{4})",
    'Goods Total': r"GOODS TOTAL (\d+\.\d+)",
    'VAT Total': r"VAT TOTAL (\d+\.\d+)",
    'Invoice Total': r"INVOICE TOTAL (\d+\.\d+)"}
    


    # Initialize an empty dictionary to store extracted values
    extracted_values = {}

    # Iterate through patterns and extract values using regex
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            extracted_values[key] = match.group(1)
        else:
            extracted_values[key] = None

    # Create DataFrame from extracted values
    invoice_df = pd.DataFrame([extracted_values])
    return invoice_df
def information_retrieve(text):
    # columns = ['Item ID', 'Document Owner', 'Type', 'Date', 'Supplier', 'Purchase Order Number', 'Document Reference',
    #            'Due Date', 'Category', 'Customer', 'Description', 'Currency', 'Total Amount', 'Tax', 'Tax Amount',
    #            'Net Amount']
    columns = ['VAT Reg No','Company Reg No', 'Invoice No', 'Date', 'Payment Due','Goods Total', 'VAT Total', 'Invoice Total']
    # columns = ['VAT Reg No', 'Company Reg No', 'Invoice No', 'Date', 'Goods Total', 'VAT Total', 'Invoice Total', 'Account Number', 'Payment Date','Payment Due', 'Page', 'Payment Reference']

    # Extract information from the text
    extracted_info = text_to_info_finder(text)
    
    # Convert the extracted information into a DataFrame
    # df = pd.DataFrame([extracted_info], columns=columns)
    
    return extracted_info

def extract_text_from_file(file_data, file_type):
    if file_type == 'image':
        return extract_text_from_image(file_data)
    elif file_type == 'pdf':
        return extract_text_from_pdf(file_data)
    else:
        return ""

