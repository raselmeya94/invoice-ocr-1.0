import re
def identify_invoice_style(text):
    if "Uber Eats UK Limited" in text or "UBERGBREATS" in text:
        return "UberEats"
    elif "Deliveroo" in text or "Deliveroo Commission" in text or "Deliveroo Gross" in text:
        return "Deliveroo"
    elif "Bidfood" in text or "Bidfood Accounts" in text or "Bidfood Accounts Receivable Department" in text:
        return "Bidfood"
    elif "Packaging Express" in text or "packagingexpress.co.uk" in text or "https://www.packagingexpress.co.uk/" in text:
        return "PackagingExpress"
    elif "UK Packaging" in text or "UK Packaging Supplies Ltd" in text or "www.ukplc.co.uk" in text:
        return "UkPackaging"
    elif "Big Yellow Self Storage Company M Limited" in text or "www. bigyellow.co.uk" in text:
        return "Big_yellow_storage"
    elif "Semrush" in text or "Semrush Inc." in text or "www.semrush.com" in text:
        return "Semrush"
    elif "METONI LOGISTICS" in text or "metonilogistics.co.uk" in text:
        return "MetoniLogistc"
    elif "Kite Packaging" in text or "Kite Packaging Ltd" in text or "kitepackaging.co.uk" in text:
        return "KitePackaging"
    elif "Waste Managed Limited" in text or "wastemanaged.co.uk" in text:
        return "WasteManaged"
    elif "Dext Software Limited" in text or "support@dext.com" in text or "www.dext.com" in text:
        return "Dext_App"
    elif "amazon" in text or "Amazon Marketing Services" in text or "AMS - Amazon Online UK Limited" in text:
        return "Amazon"
    elif "Subway International BV" in text:
        return "subway"
    elif "THE KNIGHT PRINTING" in text or "THE KNIGHT PRINTING LIMITED" in text or "theknightprinting.co.uk" in text:
        return "THE KNIGHT"



# Define patterns for different invoice styles
patterns_uber_eats = {
            'Date': r"Invoice\sdate:\s*(\d+\s\w+\s\d{4})",
            'Invoice Number': r"Invoice\snumber:\s*([A-Za-z0-9-]+)",
            'Due Date': r"Payment\sDue\s*:\s*(\d{2}\s\w+\s\d{4})",
            'Total Amount': r"Total\samount\spayable\s*£(\d+\.\d{2})",
            'Tax Amount': r"Total\sVAT\s20%\s*£(\d+\.\d{2})",
            'Net Amount': r"Total\snet\samount\s*£(\d+\.\d{2})"
}


patterns_packaging_express = {
            'Date': r'(\d{2}/\d{2}/\d{2})',
            'Invoice Number': r"Order\s#\s*(\d+)",
            'Document Reference': r"(?:InvoiceNo|invoiceNo|Invoice No|Invoice Number|Invoice \#)\s*([A-Za-z0-9]+)|INV\d{6}|d{9}|\bINV\d{6}\b",
            'Due Date': r"Payment Due\:\s*\n?\s*(\d{2}/\d{2}/\d{4})",
            'Total Amount': r'(?:Grand\sTotal|Total)\s*£(\d+\.\d{2})',
            'Tax Amount': r'VAT\s*£(\d+\.\d{2})',
            'Net Amount': r"Subtotal\s*£(\d+\.\d{2})"
}

pattern_Delivaroo = {
            'Date': r"Issue date:\s*([\w, ]+\d{4})",
            'Invoice Number': r"Invoice Serial Number:\s*([A-Za-z0-9-]+)",
            'Due Date': r"Payment Due\s*:\s*(\d{2}\s\w+\s\d{4})",
            'Total Amount': r"Invoice Total\s*\nTotal \(\£\)\n*\s*£(\d+\.\d{2})",
            'Tax Amount': r"Invoice Total\s*\nVAT Amount \(\£\)\n*\s*£(\d+\.\d{2})",
            'Net Amount': r"Invoice Total\s*\nNet \(\£\)\n*\s*£(\d+\.\d{2})"
}
patterns_uk_packaging = {
            'Date': r"(\d{2}/\d{2}/\d{2})",
            'Invoice Number': r"INV(\d{6})",
            'Due Date': r"(\d{2}/\d{2}/\d{2})",
            'Total Amount': r"£(\d+\.\d{2})",
            'Tax Amount': r"(\d+\.\d{2})\nVAT",
            'Net Amount': r"£(\d+\.\d{2})"
}
pattern_Bigyellowstorage = {
            'Date': r"Date/Tax Point\s*(\d{2}/\d{2}/\d{4})",#r"(\d{2}/\d{2}/\d{4})\s*Date/Tax Point",
            'Invoice Number': r"([A-Z0-9]+)\s*Invoice Number",
            'Due Date': r"Payment Due:\s*(\d{2}/\d{2}/\d{4})",
            'Total Amount': r"Invoice Total\s*£([\d,]+\.\d{2})",
            'Tax Amount': r"VAT @ 20%\s*£([\d,]+\.\d{2})", # Failed
            'Net Amount': r"Net Total\s*£([\d,]+\.\d{2})"  # Failed
}

patterns_semrush = {
            'Date': r"ACTIVATION\sDATE:\s*(\d{4}-\d{2}-\d{2})",
            'Invoice Number': r"INVOICE:\s*\n*#([\w\d]+)",
            'Total Amount': r"TOTAL\sAT\sCHECKOUT\s*\$([\d.]+)",
            'Tax Amount': r"VAT \(20%\)\s*\$([\d.]+)",
            'Net Amount': r"PURCHASES\s*\$([\d.]+)"

}
patterns_MetoniLogistc = {
            'Invoice Date': r"Invoice\sDate\s*(\d+\s\w+\s\d{4})",
            'Invoice Number': r"Invoice\sNumber\s*([A-Za-z0-9-]+)",
            'Due Date': r"Due\sDate:\s*(\d+\s\w+\s\d{4})",
            'Total Amount': r"TOTAL\sGBP\s*(\d+\.\d{2})",
            'Tax Amount': r"VAT \(20%\)\s*\$([\d.]+)",
            'Net Amount': r"Subtotal\s+(\d+\.\d{2})"
}

patterns_kite_packaging = {
            'Invoice Date': r'Order date:\s*(\d{2}/\d{2}/\d{4})',
            'Invoice Number': r'Order number:\s*(\d+)',
            'Total Amount': r'Grand total:\s*£(\d+\.\d{2})',
            'Tax Amount': r'Sub total:\s*[\d\.]+\s*kg\s*£[\d\.]+\s*£(\d+\.\d{2})',
            'Net Amount': r'Sub total:\s*[\d\.]+\s*kg\s*£(\d+\.\d{2})',
}

patterns_waste_managed = {
            'Invoice Date': r'Invoice Date:\s*(\d{2}/\d{2}/\d{4})',
            'Invoice Number': r'Invoice Number:\s*(WM-\d+)',
            'Due Date': r'Payment Due Date:\s*(\d{2}/\d{2}/\d{4})',
            'Total Amount': r'Invoice Total:\s*£(\d+\.\d{2})',
            'Tax Amount': r'VAT \(20%\):\s*£(\d+\.\d{2})',
            'Net Amount': r'Net Invoice Value \(excluding VAT\):\s*£(\d+\.\d{2})'
}

patterns_Dext_app = {
            'Invoice Number': r'Invoice Number:\s*(\d+)',
            'Invoice Date': r'Invoice Date:\s*(\d{2}/\d{2}/\d{4})',
            'Subtotal': r'Subtotal £(\d+\.\d{2})',#r'Subtotal\s*£(\d+\.\d{2})',
            'Tax Total (20%)':r"Tax Total 20%\s*£([\d.]+)",#r'Tax Total \(20%\) £(\d+\.\d{2})',
            'Total': r'Total £(\d+\.\d{2})',#r'Total\s*£(\d+\.\d{2})'
    }

patterns_amazon = {
            'Invoice Date': r'Invoice Date:\s*(\d{2}/\d{2}/\d{4})',
            'Invoice Number': r'Invoice Number:\s*([A-Z0-9\-]+)',
            'Subtotal': r'TOTAL.*?GBP\s*([\d,]+\.\d{2})\s*GBP\s*[\d,]+\.\d{2}\s*GBP\s*[\d,]+\.\d{2}',
            'Total VAT': r'TOTAL.*?GBP\s*[\d,]+\.\d{2}\s*GBP\s*([\d,]+\.\d{2})\s*GBP\s*[\d,]+\.\d{2}',
            'Net Amount': r'TOTAL.*?GBP\s*[\d,]+\.\d{2}\s*GBP\s*[\d,]+\.\d{2}\s*GBP\s*([\d,]+\.\d{2})'
}

# patterns_knight_printing = {
#             'Invoice Number': r'Invoice no:\s*([A-Z0-9\-]+)',
#             'Invoice Date': r'Order Date:\s*(\d{2}/\d{2}/\d{4})',
#             'Subtotal': r'Sub Total\s*£(\d+(?:,\d{3})*\.\d{2})',
#             'Total VAT': r'VAT Total\s*£(\d+\.\d{2})',
#             'Net Amount': r'Total\s*£(\d+(?:,\d{3})*\.\d{2})(?!.*Sub Total)',
#         }


# Add more pattern dictionaries for other invoice styles
patterns_knight_printing = {
    'Invoice Number': r'Invoice no:\s*([A-Z0-9\-]+)',
    'Invoice Date': r'Order Date:\s*(\d{2}/\d{2}/\d{4})',
    # 'Subtotal': r'Sub Total\s*:?\s*£(\d+\.\d{2})',  # Allow optional colon after Sub Total
    # 'Total VAT': r'VAT Total\s*:?\s*£(\d+\.\d{2})',  # Allow optional colon after VAT Total
    # 'Net Amount': r'Total\s*:?\s*£(\d+\.\d{2})',    # Allow optional colon after Total
    # 'Sub Total': r'Sub Total\s*£(\d+(?:,\d{3})*\.\d{2})', #r'^Sub Total\s*£(\d+\.\d{2})$',
    # 'VAT Total': r'VAT Total\s*:?\s*£(\d+\.\d{2})',#r'^VAT Total\s*£(\d+\.\d{2})$',
    # 'Total': r'(?:Sub\s+Total\s+£\d+\.\d{2}\s+VAT\s+Total\s+£\d+\.\d{2}\s+)?Total\s*:?\s*£(\d+\.\d{2})'#r'(\d+\.\d{2})\s+Total\s*:?\s*£(\d+\.\d{2})'
'Sub Total': r"\bSub\s+Total\s+£([\d,]+\.\d{2})\b",
    'VAT Total': r"\bVAT\s+Total\s+£([\d,]+\.\d{2})\b",
    'Total': r"\bTotal\s+£([\d,]+\.\d{2})(?!.*Total)\b",# r'total (\d+)(?!.*total)
}

def text_to_info_finder(text ):

    # Normalize the text by removing extra spaces and replacing known issues
    text = " ".join(text.strip().split('\n'))
    print("Extracted Text: ", text)
    # Remove special characters
    special_chars = ['¢', '(', ')']
    for char in special_chars:
        text = text.replace(char, '')

    final_details = {}
    invoice_style = identify_invoice_style(text)
    patterns = {}
    if invoice_style == "UberEats":
        patterns = patterns_uber_eats
    elif invoice_style == "PackagingExpress":
        patterns = patterns_packaging_express
    elif invoice_style == "Deliveroo":
        patterns = pattern_Delivaroo
    elif invoice_style == "UkPackaging":
        patterns = patterns_uk_packaging
    elif invoice_style == "Big_yellow_storage":
        patterns = pattern_Bigyellowstorage
    elif invoice_style == "Semrush":
        patterns = patterns_semrush
    elif invoice_style == "MetoniLogistc":
        patterns = patterns_MetoniLogistc
    elif invoice_style == "KitePackaging":
        patterns = patterns_kite_packaging
    elif invoice_style == "WasteManaged":
        patterns = patterns_waste_managed
    elif invoice_style == "Dext_App":
        patterns = patterns_Dext_app
    elif invoice_style == "Amazon":
        patterns = patterns_amazon
    elif invoice_style == "THE KNIGHT":
        patterns = patterns_knight_printing
    # Add more conditions for other invoice styles

    details = {"Document Type": "Invoice", "Suppliers Name": invoice_style}

    # Extract information using the identified patterns
    for key, pattern in patterns.items():
        match = re.search(pattern, text , re.DOTALL)

        if match:
            details[key] = match.group(1)
        else:
            details[key] = None

    final_details.update(details)
    print("Invoice Details:" , final_details)
    return final_details