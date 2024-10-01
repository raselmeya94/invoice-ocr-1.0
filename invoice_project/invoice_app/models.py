from django.db import models
# from .utils import extract_text_from_file
from .utils import extract_text_from_file , info_to_dataframe
import json

import json
import pandas as pd

class Invoice_Extractor(models.Model):
    def file_to_text_info(self, file_data, file_type):
        try:
            # Extract text and info from the file
            extracted_text, info = extract_text_from_file(file_data, file_type)
            informations = info_to_dataframe(info) 

            # Convert the DataFrame to a JSON serializable format (dictionary)
            if informations is not None:
                informations_dict = informations.to_dict(orient='records')  # Convert DataFrame to list of dicts
            else:
                informations_dict = None

            # Prepare the response dictionary
            response_dict = {
                'extracted_text': extracted_text,
                'information': informations_dict
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
