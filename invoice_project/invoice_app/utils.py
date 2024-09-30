# #utils.py
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
#
# # checking document type ( is_scanned or not)
# def detect_document_type(pdf_data):
#     try:
#         pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
#         for page_num in range(len(pdf_document)):
#             page = pdf_document.load_page(page_num)
#             if len(page.get_text("text").strip()) == 0:  # Check if page contains no text
#                 return True  # Scanned PDF
#         return False  # Original PDF
#     except Exception as e:
#         print(f"Error detecting document type: {e}")
#         return False
#
# # def pdf_to_images(pdf_data):
# #     try:
# #         pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
# #         images_text = ""
# #         for page_num in range(pdf_document.page_count):
# #             page = pdf_document.load_page(page_num)
# #             pix = page.get_pixmap(matrix=fitz.Matrix(800 / 100, 800 / 100))  # Increase resolution with matrix
# #             image_data = pix.tobytes(output="jpg")
# #             images_text += extract_text_from_image(image_data)
# #         return images_text
# #     except Exception as e:
# #         print(f"Error converting PDF to images: {e}")
# #         return ""
#
# def extract_text_from_image(image_data):
#     image = Image.open(io.BytesIO(image_data))
#     image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     denoised = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)
#     text = pytesseract.image_to_string(denoised)
#
#
#     return text
#
#
# # 2nd way
# # def extract_text_from_image(image_data):
# #     # Load image from bytes and convert to OpenCV format
# #     image = Image.open(io.BytesIO(image_data))
# #     image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV
#
# #     # Resize the image to improve resolution
# #     scale_percent = 350  # Increase the resolution by 50%
# #     width = int(image.shape[1] * scale_percent / 100)
# #     height = int(image.shape[0] * scale_percent / 100)
# #     dim = (width, height)
# #     resized = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)
#
# #     # Convert to grayscale
# #     gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
#
# #     # Apply Gaussian blur to reduce noise
# #     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#
# #     # Remove the background using morphological operations
# #     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
# #     blackhat = cv2.morphologyEx(blurred, cv2.MORPH_BLACKHAT, kernel)
#
# #     # Combine original gray and background removed image
# #     corrected = cv2.add(gray, blackhat)
#
# #     # Apply Otsu's thresholding to binarize the image
# #     _, binary = cv2.threshold(corrected, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
# #     # Apply denoising
# #     denoised = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)
#
# #     # Define custom configuration for Tesseract OCR
# #     # custom_config = r'--oem 3 --psm 6'  # Use OEM 3 (default) and PSM 6 (assumes a single uniform block of text)
#
# #     # Extract text from the preprocessed image
# #     text = pytesseract.image_to_string(denoised)
#
# #     return text
# # def extract_text_from_pdf_img(pdf_data):
# #     pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
# #     text = ""
# #     for page_num in range(len(pdf_document)):
# #         page = pdf_document.load_page(page_num)
# #         pix = page.get_pixmap()
# #         image_data = pix.tobytes(output="png")
# #         text += extract_text_from_image(image_data)
# #     return text
#
# def extract_text_from_pdf(pdf_data):
#     pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
#     text = ""
#     for page_num in range(len(pdf_document)):
#         page = pdf_document.load_page(page_num)
#         text += page.get_text("text")
#
#     if len(text)<100:
#         for page_num in range(len(pdf_document)):
#             page = pdf_document.load_page(page_num)
#             pix = page.get_pixmap()
#             image_data = pix.tobytes(output="png")
#             text += extract_text_from_image(image_data)
#     return text
#
#
# def text_to_info_finder(text):
#     # Normalize the text by removing extra spaces and replacing known issues
#     text = ' '.join(text.split())
#     # text = text.replace('ate', 'Date')
#     print("Extracted Text: ", text)
#     # Remove special characters
#     special_chars = ['¢', '(', ')']
#     for char in special_chars:
#         text = text.replace(char, '')
#
#     document_type = "OTHER"
#     # Determine document type
#     if "TIN Certificate" in text or "Taxpayer's Identification Number (TIN) Certificate" in text:
#         document_type = "TIN"
#     elif "Value Added Tax" in text or "Value Added Tax Registration Certificate" in text or "Customs, Excise and VAT Commissionerate" in text:
#         document_type="VAT"
#     elif "Certificate of Incorporation" in text or " incorporated\nunder the Companies Act" in text:
#         document_type="INCORPORATE"
#     else:
#         document_type="Invoice"
#
#     final_details = {}
#     # Handle TIN Certificate
#     if document_type == "TIN":
#         tin_number = re.search(r'TIN\s*:\s*(\d+)', text)
#         company_name = re.search(r'Name\s*:\s*(.+?)\s*\d+\s*Registered Address/Permanent Address\s*:', text, re.DOTALL)
#         registered_address = re.search(r'Registered Address/Permanent Address\s*:\s*(.+?)\s*\d+\s*Current Address\s*:', text, re.DOTALL)
#         current_address = re.search(r'Current Address\s*:\s*(.+?)\s*\d+\s*Previous TIN\s*:', text, re.DOTALL)
#         previous_tin = re.search(r'Previous TIN\s*:\s*(.+?)\s*\d+\s*Status\s*:', text, re.DOTALL)
#         status =re.search(r'Status\s*:\s*(.+?)\s*Date\s*:', text, re.DOTALL)
#         date = re.search(r'Date\s*:\s*(.+?)\s*Please Note:', text, re.DOTALL)
#
#         details = {
#             'Document Type': 'TIN Certificate',
#             'TIN': tin_number.group(1) if tin_number else None,
#             # 'Registration Number': registration_number.group(1) if registration_number else None,
#             'Company Name': company_name.group(1).strip() if company_name else None,
#             'Registered Address': registered_address.group(1).strip() if registered_address else None,
#             'Current Address': current_address.group(1).strip() if current_address else None,
#             'Previous TIN': previous_tin.group(1) if previous_tin else None,
#             'Status': status.group(1) if status else None,
#             'date' : date.group(1).strip() if date else None
#         }
#
#         final_details.update(details)
#
#     elif document_type=="VAT":
#
#         BIN = re.search(r"BIN\s*:?\s*(\d{9}-\d{4})", text, re.DOTALL)
#         name_of_entity = re.search(r"Name\s+of\s+the\s+Entity\s*:?\s*(.*?)(?= Trading)", text, re.DOTALL)
#         trading_brand_name = re.search(r"Trading\s+Brand\s+Name\s*:?\s*(.*)(?= Old)", text, re.DOTALL)
#         old_bin = re.search(r"Old\s+BIN\s*:?\s*(\d+)", text)
#         etin = re.search(r"e-TIN\s*:?\s*(\d+)", text)
#         # etin = re.search(r"(?:e-TIN\s*:?\s*(\d+))|((\d+)\s*e-TIN)", text)
#         address = re.search(r"Address\s*:?\s*(.*?);.*?$", text, re.DOTALL)
#         issue_date = re.search(r"Issue Date\s*:?\s*(\d{2}/\d{2}/\d{4})", text)
#         effective_date = re.search(r"(?:Bfective Date|Effective Date)\s*:?\s*(\d{2}/\d{2}/\d{4})", text)
#         type_of_ownership = re.search(r"Type\s+of\s+Ownership\s*:?\s*(.*?)(?=Major)", text, re.DOTALL)
#         major_area_of_activity = re.search(r"Major\s+Area\s+of\s+Economic\s+Activity\s*:?\s*(.*?)(?=This)", text, re.DOTALL)
#
#         details = {
#             'Document Type': 'VAT Certificate',
#             'BIN': BIN.group(1) if BIN else None,
#             'Name of the Entity': name_of_entity.group(1).strip() if name_of_entity else None,
#             'Trading Brand Name': trading_brand_name.group(1).strip() if trading_brand_name else None,
#             'Old BIN': old_bin.group(1) if old_bin else None,
#             'e-TIN': etin.group(1) if etin else None,
#             'Address': address.group(1).strip() if address else None,
#             'Issue Date': issue_date.group(1) if issue_date else None,
#             'Effective Date': effective_date.group(1) if effective_date else None,
#             'Type of Ownership': type_of_ownership.group(1).strip() if type_of_ownership else None,
#             'Major Area of Economic Activity': major_area_of_activity.group(1).strip() if major_area_of_activity else None,
#         }
#         final_details.update(details)
#
#
#
#     elif document_type=="INCORPORATE":
#         certificate_no = re.search(r"No\.?\s*(C-\d+/\d{4})", text, re.DOTALL)
#         company_name = re.search(r"I hereby certify that\s+(.*?)\s+is", text, re.DOTALL)
#         date_of_incorporation = re.search(r"Date:\s*(\d{2}/\d{2}/\d{4})", text, re.DOTALL)
#         limited_company_type = re.search(r"that the Company is\s+(Limited|Private Limited)", text, re.DOTALL)
#         issue_no = re.search(r"Issue\s+No\.\s*(\d+)", text, re.DOTALL)
#         issue_date = re.search(r"Date:\s*(\d{2}/\d{2}/\d{4})", text, re.DOTALL)
#
#         details = {
#             'Document Type': 'Incorporation Certificate',
#             'Certificate No.': certificate_no.group(1).strip() if certificate_no else None,
#             'Company Name': company_name.group(1).strip() if company_name else None,
#             'Date of Incorporation': date_of_incorporation.group(1) if date_of_incorporation else None,
#             'Company Type': limited_company_type.group(1) if limited_company_type else None,
#             'Issue Number': issue_no.group(1) if issue_no else None,
#             'Issue Date': issue_date.group(1) if issue_date else None,
#         }
#
#         final_details.update(details)
#
#     elif document_type=="Invoice":
#         if "Uber Eats UK Limited" in text or "UBERGBREATS" in text:
#             supplier = "UberEats"
#         elif "Deliveroo" in text or "Deliveroo Commission" in text or "Deliveroo Gross" in text:
#             supplier = "Deliveroo"
#         elif "Bidfood" in text or "Bidfood Accounts" in text or "Bidfood Accounts Receivable Department" in text:
#             supplier = "Bidfood"
#         elif "Packaging Express" in text or "packagingexpress.co.uk" in text or "https://www.packagingexpress.co.uk/" in text:
#             supplier = "PackagingExpress"
#         elif "UK Packaging" in text or "UK Packaging Supplies Ltd" in text or "www.ukplc.co.uk" in text:
#             supplier = "UkPacking"
#         elif "Big Yellow Self Storage Company M Limited" in text or "www. bigyellow.co.uk" in text:
#             supplier = "Bigyellowstorage"
#         elif "Semrush" in text or "Semrush Inc." in text or "www.semrush.com" in text:
#             supplier = "Semrush"
#         elif "METONI LOGISTICS" in text or "metonilogistics.co.uk" in text:
#             supplier = "METONILogistc"
#         elif "Kite Packaging" in text or "Kite Packaging Ltd" in text or "kitepackaging.co.uk" in text:
#             supplier = "KitePackaging"
#         elif "Waste Managed Limited" in text or "wastemanaged.co.uk" in text:
#             supplier = "WasteManaged"
#         elif "Dext Software Limited" in text or "support@dext.com" in text or "www.dext.com" in text:
#             supplier = "Dext"
#         elif "amazon" in text or "Amazon Marketing Services" in text or "AMS - Amazon Online UK Limited" in text:
#             supplier = "Amazon"
#         elif "Subway International BV" in text:
#             supplier = "subway"
#         elif "THE KNIGHT PRINTING" in text or "THE KNIGHT PRINTING LIMITED" in text or "theknightprinting.co.uk" in text:
#             supplier = "THEKNIGHTPRINT"
#
#
#
#
#
#
#
#         details={"Document Type":"Invoice"}
#         patterns = {
#             'Date': r"Order\sDate:\s*(\b\d{1,2} \w+ \d{4}\b)",
#             'Purchase Order Number':r"Order\s#\s*(\d+)",
#             'Document Reference': r"(?:InvoiceNo|invoiceNo|Invoice No|Invoice Number|Invoice \#)\s*([A-Za-z0-9-]+)|INV\d{6}|d{9}|\bINV\d{6}\b",
#             'Due Date': r"(?:Due\sDate:|Due\sDate|Payment\sDue:)\s*(?:(\d{2}/\d{2}/\d{2,4})|(\d{1,2}\s+[A-Za-z]+\s+\d{4}))",
#             # 'Customer':
#             # 'Currency':'GBP',
#             'Total Amount': r'Grand\sTotal\s*£(\d+\.\d{2})',
#             'Tax Amount': r'VAT\s*£(\d+\.\d{2})',
#             'Net Amount': r"Subtotal\s*£(\d+\.\d{2})"
#
#         }
#
#         # r"(?:Due Date:|Due\sDate|Payment Due:)\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})|(\d{2}/\d{2}/\d{2,4})", #r"Payment Due\:\s*\n?\s*(\d{2}/\d{2}/\d{4})",
#         # Initialize an empty dictionary to store extracted values
#         # List of possible supplier names
#         supplier_names = [
#             "packagingexpress",
#             "packaging express",
#             "Bidfood",
#             "UK Packaging Supplies Ltd",
#             "Big Yellow Self Storage Company M Limited",
#             "Metoni Logistics",
#             "Arte Regal Import S.L."
#         ]
#
#         # Check if any of the supplier names are present in the text
#         found_supplier = False
#         for supplier in supplier_names:
#             if re.search(re.escape(supplier), text, re.IGNORECASE):
#                 details['Supplier'] = supplier
#                 found_supplier = True
#                 break
#
#         if not found_supplier:
#             details['Supplier'] = None
#
#         # Dictionary mapping currency symbols to their names or codes
#         currency_mapping = {
#             "GBP": "GBP",
#             '€': "EURO",
#             '£': "GBP",
#         }
#         # Check for currency symbols in the text and assign the corresponding value
#         for symbol, currency in currency_mapping.items():
#             if re.search(re.escape(symbol), text):
#                 details['Currency'] = currency
#                 break
#         else:
#             details['Currency'] = None
#         # Iterate through patterns and extract values using regex
#         for key, pattern in patterns.items():
#             match = re.search(pattern, text)
#             if match:
#                 details[key] = match.group(1)  # For other keys, extract the matched group
#             else:
#                 details[key] = None
#         final_details.update(details)
#
#     # Create DataFrame from extracted values
#     # invoice_df = pd.DataFrame([final_info])
#
#     return final_details
#
# def information_retrieve(text):
#     # columns = ['Item ID', 'Document Owner', 'Type', 'Date', 'Supplier', 'Purchase Order Number', 'Document Reference',
#     #            'Due Date', 'Category', 'Customer', 'Description', 'Currency', 'Total Amount', 'Tax', 'Tax Amount',
#     #            'Net Amount']
#     columns = ['VAT Reg No','Company Reg No', 'Invoice No', 'Date', 'Payment Due','Goods Total', 'VAT Total', 'Invoice Total']
#     # columns = ['VAT Reg No', 'Company Reg No', 'Invoice No', 'Date', 'Goods Total', 'VAT Total', 'Invoice Total', 'Account Number', 'Payment Date','Payment Due', 'Page', 'Payment Reference']
#
#     # Extract information from the text
#     extracted_info = text_to_info_finder(text)
#
#     # Convert the extracted information into a DataFrame
#     # df = pd.DataFrame([extracted_info], columns=columns)
#
#     return extracted_info
#
# # def extract_text_from_file(file_data, file_type):
# #     if file_type == 'image':
# #         return extract_text_from_image(file_data)
# #     elif file_type == 'pdf':
# #         return extract_text_from_pdf(file_data)
# #     else:
# #         return ""
#
# def extract_text_from_file(file_data, file_type):
#     try:
#         if file_type == 'image':
#             return extract_text_from_image(file_data)
#         elif file_type == 'pdf':
#
#             if detect_document_type(file_data):
#
#                 return pdf_to_page_extract(file_data)
#             else:
#                 return pdf_to_page_extract(file_data)
#
#         else:
#             return ""
#     except Exception as e:
#         print(f"Error extracting text from file: {e}")
#         return ""
#
#
#
# ###
# # def pdf_to_page_extract(file_data):
# #   # Convert PDF pages to images
# #   pages = convert_from_path(file_data)
# #   images_text = ""
# #
# #   # Save each page as a rotated image
# #   for i, page in enumerate(pages, start=1):
# #       with BytesIO() as image_stream:
# #         page.save(image_stream, format='JPEG')
# #         image_stream.seek(0)  # Rewind the stream to the beginning
# #         # Use image_stream for further processing, e.g., passing it to your table extraction function
# #         images_text += extract_text_from_image(image_stream)
# #         return images_text
# def pdf_to_page_extract(file_data):
#     try:
#         pages = convert_from_bytes(file_data)
#         images_text = ""
#         for page in pages:
#             with BytesIO() as image_stream:
#                 page.save(image_stream, format='JPEG')
#                 image_stream.seek(0)
#                 images_text += extract_text_from_image(image_stream.getvalue())
#         return images_text
#     except Exception as e:
#         print(f"Error extracting text from PDF images: {e}")
#         return ""



##########


import io
import re
from PIL import Image
import cv2
import pytesseract
import fitz  # PyMuPDF
import pandas as pd
import numpy as np
from pdf2image import convert_from_bytes
from io import BytesIO


# checking document type (is_scanned or not)
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

def ignore_lines(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to create a binary image
    ret, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    ret = min(255, int(1.5 * ret))

    # Dilation to connect pixels in weak images
    structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 2))
    x = cv2.dilate(bw, structure, iterations=1)
    y = bw

    # Applying dilation on vertical lines
    rows = x.shape[0]
    vertical_size = rows // 80
    vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))

    # Apply morphology operations to detect vertical lines
    x = cv2.erode(x, vertical_structure)
    x = cv2.dilate(x, vertical_structure)

    # Applying dilation to horizontal lines
    cols = y.shape[1]
    horizontal_size = cols // 90
    horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))

    # Apply morphology operations to detect horizontal lines
    y = cv2.erode(y, horizontal_structure)
    y = cv2.dilate(y, horizontal_structure)

    # Combine vertical and horizontal lines
    lines_mask = cv2.add(x, y)

    # Remove lines by setting them to white in the original image
    gray[lines_mask == 255] = 255

    return gray
# def extract_text_from_image(image_data):
#     image = Image.open(io.BytesIO(image_data))
#     image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     denoised = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)
#
#     # Extract text from the preprocessed image
#     text = pytesseract.image_to_string(denoised, lang='eng')
#
#     return text

# Function to stretch columns (used in ignore_lines)


def adjust_brightness_contrast(image, alpha, beta):
    return cv2.addWeighted(image, alpha, image, 0, beta)

def extract_text_from_image(image_data):
    # Load image from bytes and convert to OpenCV format
    image = Image.open(io.BytesIO(image_data))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV

    enhanced_image = adjust_brightness_contrast(image, 1, 50)
    # Save the enhanced image for debugging or further use
    enhanced_image_path = "enhanced_image.png"
    cv2.imwrite(enhanced_image_path, enhanced_image)
    #
    # remove_imaged= ignore_lines(enhanced_image)
    # cv2.imwrite("remove_image.png", remove_imaged)
    # Extract text from the preprocessed image
    text = pytesseract.image_to_string(enhanced_image_path, lang = 'eng')
    return text

def extract_text_from_pdf(pdf_data):
    pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")

    if len(text) < 100:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            image_data = pix.tobytes(output="png")
            text += extract_text_from_image(image_data)
    return text

#
# def identify_invoice_style(text):
#     if "Uber Eats UK Limited" in text or "UBERGBREATS" in text:
#         return "UberEats"
#     elif "Deliveroo" in text or "Deliveroo Commission" in text or "Deliveroo Gross" in text:
#         return "Deliveroo"
#     elif "Bidfood" in text or "Bidfood Accounts" in text or "Bidfood Accounts Receivable Department" in text:
#         return "Bidfood"
#     elif "Packaging Express" in text or "packagingexpress.co.uk" in text or "https://www.packagingexpress.co.uk/" in text:
#         return "PackagingExpress"
#     elif "UK Packaging" in text or "UK Packaging Supplies Ltd" in text or "www.ukplc.co.uk" in text:
#         return "UkPackaging"
#     elif "Big Yellow Self Storage Company M Limited" in text or "www. bigyellow.co.uk" in text:
#         return "Big_yellow_storage"
#     elif "Semrush" in text or "Semrush Inc." in text or "www.semrush.com" in text:
#         return "Semrush"
#     elif "METONI LOGISTICS" in text or "metonilogistics.co.uk" in text:
#         return "MetoniLogistc"
#     elif "Kite Packaging" in text or "Kite Packaging Ltd" in text or "kitepackaging.co.uk" in text:
#         return "KitePackaging"
#     elif "Waste Managed Limited" in text or "wastemanaged.co.uk" in text:
#         return "WasteManaged"
#     elif "Dext Software Limited" in text or "support@dext.com" in text or "www.dext.com" in text:
#         return "Dext_App"
#     elif "amazon" in text or "Amazon Marketing Services" in text or "AMS - Amazon Online UK Limited" in text:
#         return "Amazon"
#     elif "Subway International BV" in text:
#         return "subway"
#     elif "THE KNIGHT PRINTING" in text or "THE KNIGHT PRINTING LIMITED" in text or "theknightprinting.co.uk" in text:
#         return "THEKNIGHTPRINT"
#
#
#
# # Define patterns for different invoice styles
# patterns_uber_eats = {
#             'Date': r"Invoice\sdate:\s*(\d+\s\w+\s\d{4})",
#             'Invoice Number': r"Invoice\snumber:\s*([A-Za-z0-9-]+)",
#             'Due Date': r"Payment\sDue\s*:\s*(\d{2}\s\w+\s\d{4})",
#             'Total Amount': r"Total\samount\spayable\s*£(\d+\.\d{2})",
#             'Tax Amount': r"Total\sVAT\s20%\s*£(\d+\.\d{2})",
#             'Net Amount': r"Total\snet\samount\s*£(\d+\.\d{2})"
# }
#
#
# patterns_packaging_express = {
#             'Date': r'(\d{2}/\d{2}/\d{2})',
#             'Invoice Number': r"Order\s#\s*(\d+)",
#             'Document Reference': r"(?:InvoiceNo|invoiceNo|Invoice No|Invoice Number|Invoice \#)\s*([A-Za-z0-9]+)|INV\d{6}|d{9}|\bINV\d{6}\b",
#             'Due Date': r"Payment Due\:\s*\n?\s*(\d{2}/\d{2}/\d{4})",
#             'Total Amount': r'(?:Grand\sTotal|Total)\s*£(\d+\.\d{2})',
#             'Tax Amount': r'VAT\s*£(\d+\.\d{2})',
#             'Net Amount': r"Subtotal\s*£(\d+\.\d{2})"
# }
#
# pattern_Delivaroo = {
#             'Date': r"Issue date:\s*([\w, ]+\d{4})",
#             'Invoice Number': r"Invoice Serial Number:\s*([A-Za-z0-9-]+)",
#             'Due Date': r"Payment Due\s*:\s*(\d{2}\s\w+\s\d{4})",
#             'Total Amount': r"Invoice Total\s*\nTotal \(\£\)\n*\s*£(\d+\.\d{2})",
#             'Tax Amount': r"Invoice Total\s*\nVAT Amount \(\£\)\n*\s*£(\d+\.\d{2})",
#             'Net Amount': r"Invoice Total\s*\nNet \(\£\)\n*\s*£(\d+\.\d{2})"
# }
# patterns_uk_packaging = {
#             'Date': r"(\d{2}/\d{2}/\d{2})",
#             'Invoice Number': r"INV(\d{6})",
#             'Due Date': r"(\d{2}/\d{2}/\d{2})",
#             'Total Amount': r"£(\d+\.\d{2})",
#             'Tax Amount': r"(\d+\.\d{2})\nVAT",
#             'Net Amount': r"£(\d+\.\d{2})"
# }
# pattern_Bigyellowstorage = {
#             'Date': r"(\d{2}/\d{2}/\d{4})\s*Date/Tax Point",
#             'Invoice Number': r"([A-Z0-9]+)\s*Invoice Number",
#             'Due Date': r"Payment Due:\s*(\d{2}/\d{2}/\d{4})",
#             'Total Amount': r"Invoice Total\s*£([\d,]+\.\d{2})",
#             'Tax Amount': r"VAT @ 20%\s*£([\d,]+\.\d{2})", # Failed
#             'Net Amount': r"Net Total\s*£([\d,]+\.\d{2})"  # Failed
# }
#
# patterns_semrush = {
#             'Date': r"ACTIVATION\sDATE:\s*(\d{4}-\d{2}-\d{2})",
#             'Invoice Number': r"INVOICE:\s*\n*#([\w\d]+)",
#             'Total Amount': r"TOTAL\sAT\sCHECKOUT\s*\$([\d.]+)",
#             'Tax Amount': r"VAT \(20%\)\s*\$([\d.]+)",
#             'Net Amount': r"PURCHASES\s*\$([\d.]+)"
#
# }
# patterns_MetoniLogistc = {
#             'Invoice Date': r"Invoice\sDate\s*(\d+\s\w+\s\d{4})",
#             'Invoice Number': r"Invoice\sNumber\s*([A-Za-z0-9-]+)",
#             'Due Date': r"Due\sDate:\s*(\d+\s\w+\s\d{4})",
#             'Total Amount': r"TOTAL\sGBP\s*(\d+\.\d{2})",
#             'Tax Amount': r"VAT \(20%\)\s*\$([\d.]+)",
#             'Net Amount': r"Subtotal\s+(\d+\.\d{2})"
# }
#
# patterns_kite_packaging = {
#             'Invoice Date': r'Order date:\s*(\d{2}/\d{2}/\d{4})',
#             'Invoice Number': r'Order number:\s*(\d+)',
#             'Total Amount': r'Grand total:\s*£(\d+\.\d{2})',
#             'Tax Amount': r'Sub total:\s*[\d\.]+\s*kg\s*£[\d\.]+\s*£(\d+\.\d{2})',
#             'Net Amount': r'Sub total:\s*[\d\.]+\s*kg\s*£(\d+\.\d{2})',
# }
#
# patterns_waste_managed = {
#             'Invoice Date': r'Invoice Date:\s*(\d{2}/\d{2}/\d{4})',
#             'Invoice Number': r'Invoice Number:\s*(WM-\d+)',
#             'Due Date': r'Payment Due Date:\s*(\d{2}/\d{2}/\d{4})',
#             'Total Amount': r'Invoice Total:\s*£(\d+\.\d{2})',
#             'Tax Amount': r'VAT \(20%\):\s*£(\d+\.\d{2})',
#             'Net Amount': r'Net Invoice Value \(excluding VAT\):\s*£(\d+\.\d{2})'
# }
#
# patterns_Dext_app = {
#         'Invoice Number': r'Invoice Number:\s*(\d+)',
#         'Invoice Date': r'Invoice Date:\s*(\d{2}/\d{2}/\d{4})',
#         'Subtotal': r'Subtotal\s*£(\d+\.\d{2})',
#         'Tax Total': r'Tax Total \((\d+)%\)\s*\n\s*£([\d.]+)',
#         'Total': r'Total\s*£(\d+\.\d{2})'
#     }
#
#
# # Add more pattern dictionaries for other invoice styles
#
# def text_to_info_finder(text):
#     # Normalize the text by removing extra spaces and replacing known issues
#     text = ' '.join(text.split())
#     print("Extracted Text: ", text)
#     # Remove special characters
#     special_chars = ['¢', '(', ')']
#     for char in special_chars:
#         text = text.replace(char, '')
#
#     document_type = "OTHER"
#     # Determine document type
#     if "TIN Certificate" in text or "Taxpayer's Identification Number (TIN) Certificate" in text:
#         document_type = "TIN"
#     elif "Value Added Tax" in text or "Value Added Tax Registration Certificate" in text or "Customs, Excise and VAT Commissionerate" in text:
#         document_type = "VAT"
#     elif "Certificate of Incorporation" in text or " incorporated\nunder the Companies Act" in text:
#         document_type = "INCORPORATE"
#     else:
#         document_type = "Invoice"
#
#     final_details = {}
#
#     if document_type == "Invoice":
#         invoice_style = identify_invoice_style(text)
#         patterns = {}
#         if invoice_style == "UberEats":
#             patterns = patterns_uber_eats
#         elif invoice_style == "PackagingExpress":
#             patterns = patterns_packaging_express
#         elif invoice_style == "Deliveroo":
#             patterns = pattern_Delivaroo
#         elif invoice_style == "UkPackaging":
#             patterns = patterns_uk_packaging
#         elif invoice_style == "Big_yellow_storage":
#             patterns = pattern_Bigyellowstorage
#         elif invoice_style == "Semrush":
#             patterns = patterns_semrush
#         elif invoice_style == "MetoniLogistc":
#             patterns = patterns_MetoniLogistc
#         elif invoice_style == "KitePackaging":
#             patterns = patterns_kite_packaging
#         elif invoice_style == "WasteManaged":
#             patterns = patterns_waste_managed
#         elif invoice_style == "Dext_App":
#             patterns = patterns_Dext_app
#         # Add more conditions for other invoice styles
#
#         details = {"Document Type": "Invoice", "Invoice Style": invoice_style}
#
#         # Extract information using the identified patterns
#         for key, pattern in patterns.items():
#             match = re.search(pattern, text)
#             if match:
#                 details[key] = match.group(1)
#             else:
#                 details[key] = None
#
#         final_details.update(details)
#
#     return final_details
from .invoice_classify import text_to_info_finder

def information_retrieve(text):
    columns = ['VAT Reg No', 'Company Reg No', 'Invoice No', 'Date', 'Payment Due', 'Goods Total', 'VAT Total',
               'Invoice Total']
    extracted_info = text_to_info_finder(text)
    return extracted_info


def extract_text_from_file(file_data, file_type):
    try:
        if file_type == 'image':
            return extract_text_from_image(file_data)
        elif file_type == 'pdf':
            if detect_document_type(file_data):
                return extract_text_from_pdf(file_data)
            else:
                # return extract_text_from_pdf(file_data)
                return extract_text_from_pdf(file_data)

        else:
            return ""
    except Exception as e:
        print(f"Error extracting text from file: {e}")
        return ""


def pdf_to_page_extract123(file_data):
    try:
        pages = convert_from_bytes(file_data)
        images_text = ""
        for page in pages:
            with BytesIO() as image_stream:
                page.save(image_stream, format='JPEG')
                image_stream.seek(0)
                images_text += extract_text_from_image(image_stream.getvalue())
        return images_text
    except Exception as e:
        print(f"Error extracting text from PDF images: {e}")
        return ""
