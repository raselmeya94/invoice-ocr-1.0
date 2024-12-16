import io
import re
from PIL import Image
import cv2
import pytesseract
import fitz  # PyMuPDF
import pandas as pd
import numpy as np

def extract_text_from_image(image_data):
    try:
        image = Image.open(io.BytesIO(image_data))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        denoised = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)
        text = pytesseract.image_to_string(denoised)
        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

def detect_document_type(pdf_data):
    try:
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            if len(page.get_text("text").strip()) == 0:  # Check if page contains no text
                return True  # Scanned PDF
        return False  # Original PDF
    except Exception as e:
        print(f"Error detecting document type: {e}")
        return False

def extract_text_from_pdf(pdf_data):
    try:
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text")
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def pdf_to_images(pdf_data):
    try:
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
        images_text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(1200 / 120, 1200 / 120))  # Increase resolution with matrix
            image_data = pix.tobytes(output="jpg")
            images_text += extract_text_from_image(image_data)
        return images_text
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return ""


#---3July Pdf_to_image---#
# def extract_text_from_pdf(pdf_data):
#     try:
#         pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
#         text = ""
#
#         for page_num in range(len(pdf_document)):
#             page = pdf_document.load_page(page_num)
#             page_text = page.get_text()
#
#             # Example: Extracting "Name of the Entity"
#             entity_name_pattern = r"Name of the Entity\s*:?\s*(.*)"
#             entity_name_match = re.search(entity_name_pattern, page_text, re.IGNORECASE)
#             if entity_name_match:
#                 entity_name = entity_name_match.group(1).strip()
#                 text += f"Name of the Entity: {entity_name}\n"
#
#             # Example: Extracting "Address"
#             address_pattern = r"Address\s*:?\s*(.*)"
#             address_match = re.search(address_pattern, page_text, re.IGNORECASE)
#             if address_match:
#                 address = address_match.group(1).strip()
#                 text += f"Address: {address}\n"
#
#             # Add more sections as needed based on your document's layout and content
#
#         return text.strip()
#
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return ""

# def pdf_to_images(pdf_data):
#     try:
#         pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
#         images_text = ""
#         for page_num in range(pdf_document.page_count):
#             page = pdf_document.load_page(page_num)
#
#             # Increase resolution and convert page to pixmap
#             scaling_factor = 4.5  # Adjust this scaling factor as needed
#             pix = page.get_pixmap(matrix=fitz.Matrix(scaling_factor, scaling_factor))
#
#             # Convert pixmap to image
#             image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#
#             # Convert image to JPEG format
#             image_io = io.BytesIO()
#             image.save(image_io, format='JPEG')
#             image_data = image_io.getvalue()
#
#             # Extract text from the image
#             text = extract_text_from_image(image_data)
#             images_text += text + "\n"  # Add extracted text to the result
#
#         return images_text
#
#     except Exception as e:
#         print(f"Error converting PDF to images: {e}")
#         return ""


def extract_text_from_file(file_data, file_type):
    try:
        if file_type == 'image':
            return extract_text_from_image(file_data)
        elif file_type == 'pdf':
            if detect_document_type(file_data):
                print("Scanned PDF detected.")
                return pdf_to_images(file_data)
            else:
                return extract_text_from_pdf(file_data)
        else:
            return ""
    except Exception as e:
        print(f"Error extracting text from file: {e}")
        return ""

def text_to_info_finder(text):
    try:
        text = ' '.join(text.split())
        special_chars = ['¢', '(', ')']
        for char in special_chars:
            text = text.replace(char, '')

        # patterns = {
        #     'Date': r"Order\sDate:\s*(\b\d{1,2} \w+ \d{4}\b)",
        #     'Purchase Order Number': r"Order\s#\s*(\d+)",
        #     'Document Reference': r"(?:InvoiceNo|invoiceNo|Invoice No|Invoice Number|Invoice \#)\s*([A-Za-z0-9]+)|INV\d{6}|d{9}|\bINV\d{6}\b",
        #     'Due Date': r"Payment Due\:\s*\n?\s*(\d{2}/\d{2}/\d{4})",
        #     'Total Amount': r'(?:Grand\sTotal|Total)\s*£(\d+\.\d{2})',
        #     'Tax Amount': r'VAT\s*£(\d+\.\d{2})',
        #     'Net Amount': r"Subtotal\s*£(\d+\.\d{2})"
        # }


        patterns = {
            'Date': r"Invoice\sdate:\s*(\d+\s\w+\s\d{4})",
            'Invoice Number': r"Invoice\snumber:\s*([A-Za-z0-9-]+)",
            'Due Date': r"Payment\sDue\s*:\s*(\d{2}\s\w+\s\d{4})",
            'Total Amount': r"Total\samount\spayable\s*£(\d+\.\d{2})",
            'Tax Amount': r"Total\sVAT\s20%\s*£(\d+\.\d{2})",
            'Net Amount': r"Total\snet\samount\s*£(\d+\.\d{2})"
        }




        extracted_values = {}

        supplier_names = [
            "packagingexpress",
            "packaging express",
            "Bidfood",
            "UK Packaging Supplies Ltd",
            "Big Yellow Self Storage Company M Limited",
            "Metoni Logistics"

        ]

        found_supplier = False
        for supplier in supplier_names:
            if re.search(re.escape(supplier), text, re.IGNORECASE):
                extracted_values['Supplier'] = supplier
                found_supplier = True
                break

        if not found_supplier:
            extracted_values['Supplier'] = None

        currency_mapping = {
            "GBP": "GBP",
            '€': "EURO",
            '£': "GBP",
        }

        for symbol, currency in currency_mapping.items():
            if re.search(re.escape(symbol), text):
                extracted_values['Currency'] = currency
                break
        else:
            extracted_values['Currency'] = None

        for key, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                extracted_values[key] = match.group(1)
            else:
                extracted_values[key] = None

        invoice_df = pd.DataFrame([extracted_values])

        return invoice_df
    except Exception as e:
        print(f"Error finding info from text: {e}")
        return pd.DataFrame()

def information_retrieve(text):
    try:
        columns = ['VAT Reg No', 'Company Reg No', 'Invoice No', 'Date', 'Payment Due', 'Goods Total', 'VAT Total', 'Invoice Total']
        extracted_info = text_to_info_finder(text)
        return extracted_info
    except Exception as e:
        print(f"Error retrieving information: {e}")
        return pd.DataFrame()




########---2July---#######
# import io
# import re
# from PIL import Image
# import cv2
# import pytesseract
# import fitz  # PyMuPDF
# import pandas as pd
# import numpy as np
#
# def extract_text_from_image(image_data):
#     try:
#         image = Image.open(io.BytesIO(image_data))
#         image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#         denoised = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)
#         text = pytesseract.image_to_string(denoised)
#         return text
#     except Exception as e:
#         print(f"Error extracting text from image: {e}")
#         return ""
#
# def get_text_percentage(pdf_data):
#     try:
#         pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
#         total_page_area = 0.0
#         total_text_area = 0.0
#
#         for page in pdf_document:
#             total_page_area += abs(page.rect)
#             text_area = 0.0
#             for b in page.get_text_blocks():
#                 r = fitz.Rect(b[:4])  # rectangle where block text appears
#                 text_area += abs(r)
#             total_text_area += text_area
#         return total_text_area / total_page_area
#     except Exception as e:
#         print(f"Error calculating text percentage: {e}")
#         return 0.0
#
# def extract_text_from_pdf(pdf_data):
#     try:
#         pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
#         text = ""
#         for page_num in range(len(pdf_document)):
#             page = pdf_document.load_page(page_num)
#             text += page.get_text("text")
#         return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return ""
#
# def pdf_to_images(pdf_data):
#     try:
#         pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
#         images_text = ""
#         for page_num in range(pdf_document.page_count):
#             page = pdf_document.load_page(page_num)
#             pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))  # Increase resolution with matrix
#             image_data = pix.tobytes(output="jpg")
#             images_text += extract_text_from_image(image_data)
#         return images_text
#     except Exception as e:
#         print(f"Error converting PDF to images: {e}")
#         return ""
#
# def extract_text_from_file(file_data, file_type):
#     try:
#         if file_type == 'image':
#             return extract_text_from_image(file_data)
#         elif file_type == 'pdf':
#             text_percentage = get_text_percentage(file_data)
#             if text_percentage < 0.01:
#                 print("Scanned PDF detected.")
#                 return pdf_to_images(file_data)
#             else:
#                 return extract_text_from_pdf(file_data)
#         else:
#             return ""
#     except Exception as e:
#         print(f"Error extracting text from file: {e}")
#         return ""
#
# def text_to_info_finder(text):
#     try:
#         text = ' '.join(text.split())
#         special_chars = ['¢', '(', ')']
#         for char in special_chars:
#             text = text.replace(char, '')
#
#         patterns = {
#             'Date': r"Order\sDate:\s*(\b\d{1,2} \w+ \d{4}\b)",
#             'Purchase Order Number': r"Order\s#\s*(\d+)",
#             'Document Reference': r"(?:InvoiceNo|invoiceNo|Invoice No|Invoice Number|Invoice \#)\s*([A-Za-z0-9]+)|INV\d{6}|d{9}|\bINV\d{6}\b",
#             'Due Date': r"Payment Due\:\s*\n?\s*(\d{2}/\d{2}/\d{4})",
#             'Total Amount': r'(?:Grand\sTotal|Total)\s*£(\d+\.\d{2})',
#             'Tax Amount': r'VAT\s*£(\d+\.\d{2})',
#             'Net Amount': r"Subtotal\s*£(\d+\.\d{2})"
#         }
#
#         extracted_values = {}
#
#         supplier_names = [
#             "packagingexpress",
#             "packaging express",
#             "Bidfood",
#             "UK Packaging Supplies Ltd",
#             "Big Yellow Self Storage Company M Limited",
#             "Metoni Logistics"
#         ]
#
#         found_supplier = False
#         for supplier in supplier_names:
#             if re.search(re.escape(supplier), text, re.IGNORECASE):
#                 extracted_values['Supplier'] = supplier
#                 found_supplier = True
#                 break
#
#         if not found_supplier:
#             extracted_values['Supplier'] = None
#
#         currency_mapping = {
#             "GBP": "GBP",
#             '€': "EURO",
#             '£': "GBP",
#         }
#
#         for symbol, currency in currency_mapping.items():
#             if re.search(re.escape(symbol), text):
#                 extracted_values['Currency'] = currency
#                 break
#         else:
#             extracted_values['Currency'] = None
#
#         for key, pattern in patterns.items():
#             match = re.search(pattern, text)
#             if match:
#                 extracted_values[key] = match.group(1)
#             else:
#                 extracted_values[key] = None
#
#         invoice_df = pd.DataFrame([extracted_values])
#
#         return invoice_df
#     except Exception as e:
#         print(f"Error finding info from text: {e}")
#         return pd.DataFrame()
#
# def information_retrieve(text):
#     try:
#         columns = ['VAT Reg No', 'Company Reg No', 'Invoice No', 'Date', 'Payment Due', 'Goods Total', 'VAT Total', 'Invoice Total']
#         extracted_info = text_to_info_finder(text)
#         return extracted_info
#     except Exception as e:
#         print(f"Error retrieving information: {e}")
#         return pd.DataFrame()
