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
# remove line ( horizontal and vertical)
# def remove_lines(image):
#     # Convert image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply adaptive thresholding to get a binary image
#     binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
#                                    cv2.THRESH_BINARY, 11, 2)
    
#     # Invert the image
#     inverted_binary = cv2.bitwise_not(binary)
    
#     # Create horizontal and vertical structure elements
#     horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
#     vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    
#     # Detect horizontal lines
#     horizontal_lines = cv2.morphologyEx(inverted_binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    
#     # Detect vertical lines
#     vertical_lines = cv2.morphologyEx(inverted_binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    
#     # Subtract lines from the binary image
#     binary_without_lines = cv2.bitwise_and(inverted_binary, inverted_binary, mask=cv2.bitwise_not(horizontal_lines))
#     binary_without_lines = cv2.bitwise_and(binary_without_lines, binary_without_lines, mask=cv2.bitwise_not(vertical_lines))
    
#     # Invert the result back
#     result = cv2.bitwise_not(binary_without_lines)
    
#     return result

def extract_text_from_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # processed_image = remove_lines(image)
    denoised = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)
    
    text = pytesseract.image_to_string(denoised)
    return text

# def extract_text_from_pdf_img(pdf_data):
#     pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
#     text = ""
#     for page_num in range(len(pdf_document)):
#         page = pdf_document.load_page(page_num)
#         pix = page.get_pixmap()
#         image_data = pix.tobytes(output="png")
#         text += extract_text_from_image(image_data)
#     return text

def extract_text_from_pdf(pdf_data):
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")

    if len(text)<100:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            image_data = pix.tobytes(output="png")
            text += extract_text_from_image(image_data)
    return text


def text_to_info_finder(text):
    # Normalize the text by removing extra spaces and replacing known issues
    text = ' '.join(text.split())
    # text = text.replace('ate', 'Date')
    # Remove special characters
    special_chars = ['¢', '(', ')']
    for char in special_chars:
        text = text.replace(char, '')



    patterns = {
        'Date': r"Order\sDate:\s*(\b\d{1,2} \w+ \d{4}\b)",
        'Purchase Order Number':r"Order\s#\s*(\d+)",
        'Document Reference': r"(?:InvoiceNo|invoiceNo|Invoice No|Invoice Number|Invoice \#)\s*([A-Za-z0-9]+)|INV\d{6}|d{9}|\bINV\d{6}\b",
        'Due Date': r"Payment Due\:\s*\n?\s*(\d{2}/\d{2}/\d{4})",
        # 'Customer':
        # 'Currency':'GBP',
        'Total Amount': r'Grand\sTotal\s*£(\d+\.\d{2})',
        'Tax Amount': r'VAT\s*£(\d+\.\d{2})',
        'Net Amount': r"Subtotal\s*£(\d+\.\d{2})"

    }


    # Initialize an empty dictionary to store extracted values
    extracted_values = {}

    # List of possible supplier names
    supplier_names = [
        "packagingexpress",
        "packaging express",
        "Bidfood",
        "UK Packaging Supplies Ltd",
        "Big Yellow Self Storage Company M Limited",
        "Metoni Logistics"
    ]

   # Check if any of the supplier names are present in the text
    found_supplier = False
    for supplier in supplier_names:
        if re.search(re.escape(supplier), text, re.IGNORECASE):
            extracted_values['Supplier'] = supplier
            found_supplier = True
            break

    if not found_supplier:
        extracted_values['Supplier'] = None

    # Dictionary mapping currency symbols to their names or codes
    currency_mapping = {
        "GBP": "GBP",
        '€': "EURO",
        '£': "GBP",
    }
    # Check for currency symbols in the text and assign the corresponding value
    for symbol, currency in currency_mapping.items():
        if re.search(re.escape(symbol), text):
            extracted_values['Currency'] = currency
            break
    else:
        extracted_values['Currency'] = None
    # Iterate through patterns and extract values using regex
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            extracted_values[key] = match.group(1)  # For other keys, extract the matched group
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

