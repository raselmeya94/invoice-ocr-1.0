#utils.py
import io
import re
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
    
    document_type = "OTHER"
    # Determine document type
    if "TIN Certificate" in text or "Taxpayer's Identification Number (TIN) Certificate" in text:
        document_type = "TIN"
    elif "Value Added Tax" in text or "Value Added Tax Registration Certificate" in text or "Customs, Excise and VAT Commissionerate" in text:
        document_type="VAT"
    elif "Certificate of Incorporation" in text or " incorporated\nunder the Companies Act" in text:
        document_type="INCORPORATE"

    final_details = {}       
    # Handle TIN Certificate
    if document_type == "TIN":
        tin_number = re.search(r'TIN\s*:\s*(\d+)', text)
        company_name = re.search(r'Name\s*:\s*(.+?)\s*\d+\s*Registered Address/Permanent Address\s*:', text, re.DOTALL)
        registered_address = re.search(r'Registered Address/Permanent Address\s*:\s*(.+?)\s*\d+\s*Current Address\s*:', text, re.DOTALL)
        current_address = re.search(r'Current Address\s*:\s*(.+?)\s*\d+\s*Previous TIN\s*:', text, re.DOTALL)
        previous_tin = re.search(r'Previous TIN\s*:\s*(.+?)\s*\d+\s*Status\s*:', text, re.DOTALL)
        status =re.search(r'Status\s*:\s*(.+?)\s*Date\s*:', text, re.DOTALL)
        date = re.search(r'Date\s*:\s*(.+?)\s*Please Note:', text, re.DOTALL)

        details = {
            'Document Type': 'TIN Certificate',
            'TIN': tin_number.group(1) if tin_number else None,
            # 'Registration Number': registration_number.group(1) if registration_number else None,
            'Company Name': company_name.group(1).strip() if company_name else None,
            'Registered Address': registered_address.group(1).strip() if registered_address else None,
            'Current Address': current_address.group(1).strip() if current_address else None,
            'Previous TIN': previous_tin.group(1) if previous_tin else None,
            'Status': status.group(1) if status else None,
            'date' : date.group(1).strip() if date else None
        }

        final_details.update(details) 
    
    elif document_type=="VAT":

        BIN = re.search(r"BIN\s*:?\s*(\d{9}-\d{4})", text, re.DOTALL)
        name_of_entity = re.search(r"Name\s+of\s+the\s+Entity\s*:?\s*(.*?)(?= Trading)", text, re.DOTALL)
        trading_brand_name = re.search(r"Trading\s+Brand\s+Name\s*:?\s*(.*)(?= Old)", text, re.DOTALL)
        old_bin = re.search(r"Old\s+BIN\s*:?\s*(\d+)", text)
        etin = re.search(r"e-TIN\s*:?\s*(\d+)", text)
        # etin = re.search(r"(?:e-TIN\s*:?\s*(\d+))|((\d+)\s*e-TIN)", text)
        address = re.search(r"Address\s*:?\s*(.*?);.*?$", text, re.DOTALL)
        issue_date = re.search(r"Issue Date\s*:?\s*(\d{2}/\d{2}/\d{4})", text)
        effective_date = re.search(r"(?:Bfective Date|Efective Date)\s*:?\s*(\d{2}/\d{2}/\d{4})", text)
        type_of_ownership = re.search(r"Type\s+of\s+Ownership\s*:?\s*(.*?)(?=Major)", text, re.DOTALL)
        major_area_of_activity = re.search(r"Major\s+Area\s+of\s+Economic\s+Activity\s*:?\s*(.*?)(?=This)", text, re.DOTALL)

        details = {
            'Document Type': 'VAT Certificate',
            'BIN': BIN.group(1) if BIN else None,
            'Name of the Entity': name_of_entity.group(1).strip() if name_of_entity else None,
            'Trading Brand Name': trading_brand_name.group(1).strip() if trading_brand_name else None,
            'Old BIN': old_bin.group(1) if old_bin else None,
            'e-TIN': etin.group(1) if etin else None,
            'Address': address.group(1).strip() if address else None,
            'Issue Date': issue_date.group(1) if issue_date else None,
            'Effective Date': effective_date.group(1) if effective_date else None,
            'Type of Ownership': type_of_ownership.group(1).strip() if type_of_ownership else None,
            'Major Area of Economic Activity': major_area_of_activity.group(1).strip() if major_area_of_activity else None,
        }

        final_details.update(details)



    elif document_type=="INCORPORATE":
        certificate_no = re.search(r"No\.?\s*(C-\d+/\d{4})", text, re.DOTALL)
        company_name = re.search(r"I hereby certify that\s+(.*?)\s+is", text, re.DOTALL)
        date_of_incorporation = re.search(r"Date:\s*(\d{2}/\d{2}/\d{4})", text, re.DOTALL)
        limited_company_type = re.search(r"that the Company is\s+(Limited|Private Limited)", text, re.DOTALL)
        issue_no = re.search(r"Issue\s+No\.\s*(\d+)", text, re.DOTALL)
        issue_date = re.search(r"Date:\s*(\d{2}/\d{2}/\d{4})", text, re.DOTALL)

        details = {
            'Document Type': 'Incorporation Certificate',
            'Certificate No.': certificate_no.group(1).strip() if certificate_no else None,
            'Company Name': company_name.group(1).strip() if company_name else None,
            'Date of Incorporation': date_of_incorporation.group(1) if date_of_incorporation else None,
            'Company Type': limited_company_type.group(1) if limited_company_type else None,
            'Issue Number': issue_no.group(1) if issue_no else None,
            'Issue Date': issue_date.group(1) if issue_date else None,
        }

        final_details.update(details)
        
    elif document_type=="OTHER":
        details={}
        patterns = {
            'Date': r"Order\sDate:\s*(\b\d{1,2} \w+ \d{4}\b)",
            'Purchase Order Number':r"Order\s#\s*(\d+)",
            'Document Reference': r"(?:InvoiceNo|invoiceNo|Invoice No|Invoice Number|Invoice \#)\s*([A-Za-z0-9-]+)|INV\d{6}|d{9}|\bINV\d{6}\b",
            'Due Date': r"(?:Due\sDate:|Due\sDate|Payment\sDue:)\s*(?:(\d{2}/\d{2}/\d{2,4})|(\d{1,2}\s+[A-Za-z]+\s+\d{4}))",
            # 'Customer':
            # 'Currency':'GBP',
            'Total Amount': r'Grand\sTotal\s*£(\d+\.\d{2})',
            'Tax Amount': r'VAT\s*£(\d+\.\d{2})',
            'Net Amount': r"Subtotal\s*£(\d+\.\d{2})"

        }

        # r"(?:Due Date:|Due\sDate|Payment Due:)\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})|(\d{2}/\d{2}/\d{2,4})", #r"Payment Due\:\s*\n?\s*(\d{2}/\d{2}/\d{4})",
        # Initialize an empty dictionary to store extracted values
        # List of possible supplier names
        supplier_names = [
            "packagingexpress",
            "packaging express",
            "Bidfood",
            "UK Packaging Supplies Ltd",
            "Big Yellow Self Storage Company M Limited",
            "Metoni Logistics",
            "Arte Regal Import S.L."
        ]

        # Check if any of the supplier names are present in the text
        found_supplier = False
        for supplier in supplier_names:
            if re.search(re.escape(supplier), text, re.IGNORECASE):
                details['Supplier'] = supplier
                found_supplier = True
                break

        if not found_supplier:
            details['Supplier'] = None

        # Dictionary mapping currency symbols to their names or codes
        currency_mapping = {
            "GBP": "GBP",
            '€': "EURO",
            '£': "GBP",
        }
        # Check for currency symbols in the text and assign the corresponding value
        for symbol, currency in currency_mapping.items():
            if re.search(re.escape(symbol), text):
                details['Currency'] = currency
                break
        else:
            details['Currency'] = None
        # Iterate through patterns and extract values using regex
        for key, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                details[key] = match.group(1)  # For other keys, extract the matched group
            else:
                details[key] = None
        final_details.update(details)

    # Create DataFrame from extracted values
    # invoice_df = pd.DataFrame([final_info])

    return final_details

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

