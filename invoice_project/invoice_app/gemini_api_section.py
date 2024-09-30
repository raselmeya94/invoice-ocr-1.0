


# import io
# import re
# from PIL import Image
# import cv2
# import pytesseract
# import fitz  # PyMuPDF
# import pandas as pd
# import numpy as np
# from pdf2image import convert_from_bytes
# from io import BytesIO


# #pdf to image conversion functions
# def pdf_to_image_conversion(pdf_data):
#     pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
#     textOfpdf=""
#     for page_num in range(len(pdf_document)):
#         page = pdf_document.load_page(page_num)
#         pix = page.get_pixmap()
#         image_data = pix.tobytes(output="png")

#         textOfpdf+=image_to_text_with_gimini("extract all text clean and clear",image_data)
#     return textOfpdf

# # prompt_text=("find all information from this text and try to retirve all required information"
# #              f"Text: {image_text}"
# #              f"Required Infomartions:[Invoice Date , Invoice Number/Reference Number/ Purchase Order Number(any one is available) , Supplier's Name, Currency, Total Amount/ Total (any one is available) , Net Amount/Net Total(any one is available) , VAT / Vat Total/ Tax Amount(any)]"
# # )
# # First Calling function
# def extract_text_from_file(file_data, file_type):
#     prompt_text = (
#     "Extract the following required information from the given text and provide it in the form of a dictionary: "
#     f"Text: {image_text} "
#     "Return the information as: {"
#     "'Invoice Date': '...', "
#     "'Invoice Number / Reference Number / Purchase Order Number': '...', "
#     "'Supplier's Name': '...', "
#     "'Currency': '...', "
#     "'Total Amount / Total': '...', "
#     "'Net Amount / Net Total': '...', "
#     "'VAT / VAT Total / Tax Amount': '...'}")

#     try:
#         if file_type == 'image':
#             image_text= image_to_text_with_gimini(file_data)
#             info= image_to_text_with_gimini(prompt_text , image_text)
#             return info


#         elif file_type == 'pdf':
#                 # pdf to image conversion
#                 pdf_text=pdf_to_image_conversion(file_data)
#                 info= image_to_text_with_gimini(prompt_text , pdf_text)
#                 print("gemini info:" , info)
#                 return info
            
#         else:
#             return ""
#     except Exception as e:
#         print(f"Error extracting text from file: {e}")
#         return ""

# # Gimini API Call
# import google.generativeai as genai
# API_KEY="AIzaSyDnL3F7x_xh-BYsx_144N06FHBKhDTFCCc"
# genai.configure(api_key= API_KEY)

# def image_to_text_with_gimini(prompt, image_data):
#     # Load image from bytes and convert to OpenCV format
#     image = Image.open(io.BytesIO(image_data))
#     model = genai.GenerativeModel(model_name="gemini-1.5-flash")
#     response = model.generate_content([prompt, image])

#     return response.text

import re
import io
from PIL import Image
import pandas as pd
import fitz  # PyMuPDF
import google.generativeai as genai

# Configure Google Generative AI (Gemini)
API_KEY = "AIzaSyDnL3F7x_xh-BYsx_144N06FHBKhDTFCCc"
genai.configure(api_key=API_KEY)

# PDF to image conversion and text extraction functions
def pdf_to_image_conversion(pdf_data):
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    text_of_pdf = ""
    
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        image_data = pix.tobytes(output="png")
        
        # Step 1: Convert image to text using Gemini OCR
        text_of_pdf += image_to_text_with_gemini(image_data)
    
    return text_of_pdf


# Function to extract text and required information from the file (image/pdf)
def extract_text_from_file(file_data, file_type):
    print(file_type)
    try:
        if file_type == 'image':
            # Step 1: Extract text from the image using Gemini OCR
            image_text = image_to_text_with_gemini(file_data)
            # Step 2: Extract specific info from the text using Gemini
            info = extract_info_with_gemini(image_text)
            print(type(info))
            return image_text, info

        elif file_type == 'pdf':
            # Convert PDF to text via image conversion
            pdf_text = pdf_to_image_conversion(file_data)
            # Step 2: Extract specific info from the text using Gemini
            info = extract_info_with_gemini(pdf_text)
            print(type(info))
            return pdf_text, info

        else:
            return ""
    
    except Exception as e:
        print(f"Error extracting text from file: {e}")
        return ""


# Step 1: Convert image to text using Gemini
def image_to_text_with_gemini(image_data):
    try:
        # Load image data as an image
        image = Image.open(io.BytesIO(image_data))
        
        # Create a prompt for Gemini to extract text from the image
        prompt = "Extract all text without adding extra character from the given image."

        # Make a call to the Gemini API with the prompt and image data
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([prompt, image])
        
        return response.text if response else None
    except Exception as e:
        print(f"Error in Gemini OCR: {e}")
        return ""


# # Step 2: Extract specific information from the text using Gemini
# def extract_info_with_gemini(text):
#     try:
#         # Create a prompt to extract the required information from the text
#         prompt = (
#             "Extract the following required information from the given text and provide it in the form of a dictionary: "
#             f"Text: {text} "
#             "Return the information as: {"
#             "'Invoice Date': '...', "
#             "'Invoice Number': '...', "
#             "'Reference Number': '...', "
#             "'Purchase Order Number': '...', "
#             "'Order': '...', "
#             "'Supplier's Name': '...', "
#             "'Currency': '...', "
#             "'Total Amount': '...', "
#             "'Total': '...', "
#             "'Net Amount': '...', "
#             "'Net Total': '...', "
#             "'Subtotal': '...', "
#             "'VAT': '...'}"
#             "'VAT Total': '...'}"
#             "'Tax Amount': '...'}"
#         )

#         # Call Gemini API to extract information from the text
#         model = genai.GenerativeModel(model_name="gemini-1.5-flash")
#         response = model.generate_content([prompt])
        
#         return response.text if response else None
#     except Exception as e:
#         print(f"Error in Gemini Info Extraction: {e}")
#         return ""


# # Function to convert extracted information to a DataFrame with separate columns
# import re

# # Function to convert extracted information string to a DataFrame
# def info_to_dataframe(extracted_text):
#     try:
#         # Use regular expressions to find all required fields in the string
#         invoice_date = re.search(r"'Invoice Date': '([^']*)'", extracted_text)
#         invoice_ref = re.search(r"'Invoice Number / Reference Number / Purchase Order Number': '([^']*)'", extracted_text)
#         supplier_name = re.search(r"'Supplier's Name': '([^']*)'", extracted_text)
#         currency = re.search(r"'Currency': '([^']*)'", extracted_text)
#         total_amount = re.search(r"'Total Amount / Total': '([^']*)'", extracted_text)
#         net_amount = re.search(r"'Net Amount / Net Total': '([^']*)'", extracted_text)
#         vat_info = re.search(r"'VAT / VAT Total / Tax Amount': '([^']*)'", extracted_text)

#         # Extract the values or set to None if not found
#         row_data = {
#             'Invoice Date': invoice_date.group(1) if invoice_date else None,
#             'Invoice Number': invoice_ref.group(1) if invoice_ref else None,
#             'Reference Number': invoice_ref.group(1) if invoice_ref else None,
#             'Purchase Order Number': invoice_ref.group(1) if invoice_ref else None,
#             'Supplier\'s Name': supplier_name.group(1) if supplier_name else None,
#             'Currency': currency.group(1) if currency else None,
#             'Total Amount': total_amount.group(1) if total_amount else None,
#             'Net Amount': net_amount.group(1) if net_amount else None,
#             'VAT': vat_info.group(1) if vat_info else None,
#             'VAT Total': vat_info.group(1) if vat_info else None,
#             'Tax Amount': vat_info.group(1) if vat_info else None,
#         }

#         # Create a DataFrame with one row
#         df = pd.DataFrame([row_data])
#         return df

#     except Exception as e:
#         print(f"Error converting info to DataFrame: {e}")
#         return None


# Step 2: Extract specific information from the text using Gemini (adjusted prompt)
def extract_info_with_gemini(text):
    try:
        prompt = (
            "Extract the following required information from the given text and provide it in the form of a dictionary: "
            f"Text: {text} "
            "Return the information as: {"
            "'Invoice Date': '...', "
            "'Order Date': '...', "
            "'Invoice Number': '...', "
            "'Reference Number': '...', "
            "'Purchase Order Number': '...', "
            "'Supplier's Name': '...', "
            "'Currency': '...', "
            "'Due Date': '...', "
            "'Payment Due Date': '...', "
            "'Total Amount': '...', "
            "'Total': '...', "
            "'Invoice Total': '...', "
            "'Grand Total': '...', "
            "'Net Amount': '...', "
            "'Net Value': '...', "
            "'Net Total': '...', "
            "'Subtotal': '...', "
            "'VAT': '...', "
            "'VAT Total': '...', "
            "'TAX': '...', "
            "'Tax Amount': '...'}"
        )

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content([prompt])
        return response.text if response else None
    except Exception as e:
        print(f"Error in Gemini Info Extraction: {e}")
        return ""


# Step 3: Convert extracted information to a DataFrame with separate columns
def info_to_dataframe(extracted_text): 
    try:
        # Use regular expressions to find all required fields in the string
        invoice_date = re.search(r"'Invoice Date': '([^']*)'", extracted_text)
        order_date = re.search(r"'Order Date': '([^']*)'", extracted_text)
        invoice_number = re.search(r"'Invoice Number': '([^']*)'", extracted_text)
        reference_number = re.search(r"'Reference Number': '([^']*)'", extracted_text)
        purchase_order_number = re.search(r"'Purchase Order Number': '([^']*)'", extracted_text)
        supplier_name = re.search(r"'Supplier's Name': '([^']*)'", extracted_text)
        currency = re.search(r"'Currency': '([^']*)'", extracted_text)
        due_date = re.search(r"'Due Date': '([^']*)'", extracted_text)
        payment_due_date = re.search(r"'Payment Due Date': '([^']*)'", extracted_text)
        total_amount = re.search(r"'Total Amount': '([^']*)'", extracted_text)
        total = re.search(r"'Total': '([^']*)'", extracted_text)
        invoice_total = re.search(r"'Invoice Total': '([^']*)'", extracted_text)
        grand_total = re.search(r"'Grand Total': '([^']*)'", extracted_text)
        net_amount = re.search(r"'Net Amount': '([^']*)'", extracted_text)
        net_value = re.search(r"'Net Value': '([^']*)'", extracted_text)
        net_total = re.search(r"'Net Total': '([^']*)'", extracted_text)
        subtotal = re.search(r"'Subtotal': '([^']*)'", extracted_text)
        vat = re.search(r"'VAT': '([^']*)'", extracted_text)
        vat_total = re.search(r"'VAT Total': '([^']*)'", extracted_text)
        tax_amount = re.search(r"'Tax Amount': '([^']*)'", extracted_text)

        # Extract the values or set to None if not found, applying conditional logic
        row_data = {
            'Invoice Date': invoice_date.group(1) if invoice_date else (order_date.group(1) if order_date else None),
            'Document Reference': invoice_number.group(1) if invoice_number else (
                                  reference_number.group(1) if reference_number else None),
            'Purchase Order Number': purchase_order_number.group(1) if purchase_order_number else None,
            'Supplier\'s Name': supplier_name.group(1) if supplier_name else None,
            'Currency': 'Euro' if currency and 'EUR' in currency.group(1) else (
                        'GBP' if currency and 'GBP' in currency.group(1) else currency.group(1) if currency else None),
            'Due Date': due_date.group(1) if due_date else (payment_due_date.group(1) if payment_due_date else None),
            'Total Amount': total_amount.group(1) if total_amount else (
                           total.group(1) if total else (
                           invoice_total.group(1) if invoice_total else grand_total.group(1) if grand_total else None)),
            'Net Amount': net_amount.group(1) if net_amount else (
                         net_value.group(1) if net_value else (
                         net_total.group(1) if net_total else subtotal.group(1) if subtotal else None)),
            'Tax Amount': vat_total.group(1) if vat_total else (
                         vat.group(1) if vat else tax_amount.group(1) if tax_amount else None),
        }

        # Create a DataFrame with one row
        df = pd.DataFrame([row_data])
        return df

    except Exception as e:
        print(f"Error converting info to DataFrame: {e}")
        return None