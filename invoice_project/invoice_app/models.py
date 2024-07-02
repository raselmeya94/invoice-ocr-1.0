from django.db import models
from .utils import extract_text_from_file , text_to_info_finder
import json

class Invoice_Extractor(models.Model):
    def file_to_text_info(self, file_data, file_type):
        # print(file_type)
        try:
            extracted_text = extract_text_from_file(file_data, file_type)

            informations = text_to_info_finder(extracted_text)
            
            # Prepare the response dictionary
            response_dict = {
                'extracted_text': extracted_text,
                'information': informations
                } 
            # Convert the dictionary to a JSON string
            response_json = json.dumps(response_dict)

            return response_json
        except Exception as e:
            # Handle exceptions and return an error message as JSON
            error_info = {
                'error': str(e)
            }
            return json.dumps(error_info)
