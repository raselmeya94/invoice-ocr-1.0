# views.py
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .utils import extract_text_from_file , info_to_dataframe
from django.core.files.uploadedfile import InMemoryUploadedFile
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Invoice_Extractor
import base64
import json
import magic
import imghdr
from django.conf import settings

def upload_file(request):
    data = [] # Dictionary to store data for the template
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        uploaded_files = request.FILES.getlist('files')

        # uploaded_files: InMemoryUploadedFile = form.cleaned_data['files']

        for uploaded_file in uploaded_files:
            file_data = uploaded_file.read()
            file_type = uploaded_file.content_type
            # print(uploaded_file.name )
            #

            if file_type.startswith('image'):
                file_type = 'image'
            elif file_type == 'application/pdf':
                file_type = 'pdf'
            else:
                print("Sorry File Type Don't Match")

            extracted_text , info = extract_text_from_file(file_data, file_type)
            print("info:" , info)
            encoded_file = base64.b64encode(file_data).decode('utf-8')
            # Generate DataFrame and HTML for each file
            df = info_to_dataframe(info)
            df_info=df
            df_html =df_info.to_html(index=False)
            # print(uploaded_file.size)

            data.append({
                'filename': uploaded_file.name,
                'file_size': str(round(uploaded_file.size / 1024 , 2))+" KB",
                'uploaded_file_data':encoded_file,
                'extracted_text': extracted_text,
                'file_type': file_type,
                'df_html': df_html,
            })

        return render(request, 'index.html', {'form': form, 'data': data })
    else:
        form = UploadFileForm()
        return render(request, 'index.html', {'form': form, })


# API for Another UI
@csrf_exempt
def invoice_information(request):
    if request.method == 'POST':
        try:
            # Check content length limit
            content_length = int(request.META.get('CONTENT_LENGTH', 0))
            if content_length > settings.DATA_UPLOAD_MAX_MEMORY_SIZE:
                return JsonResponse({'status': 'error', 'message': 'Total file size exceeds the limit'}, status=400)

            file_data = None
            file_type = None

            # Expecting only base64-encoded file in the request body
            if request.body:
                try:
                    data = json.loads(request.body.decode('utf-8'))
                    base64_data = data.get('file_data')
                    if base64_data:
                        # Decode the base64 string
                        file_data = base64.b64decode(base64_data)

                        # Determine file type using python-magic
                        mime = magic.Magic(mime=True)
                        file_type = mime.from_buffer(file_data)

                        if not file_type.startswith('image') and file_type != 'application/pdf':
                            return JsonResponse({"status": "error", "message": "Error: Invalid file format! Please make sure the file is an image or PDF."}, status=400)
                except (json.JSONDecodeError, base64.binascii.Error):
                    return JsonResponse({"status": "error", "message": "Error decoding base64 file. Please ensure it is properly encoded."}, status=400)
            else:
                return JsonResponse({"status": "error", "message": "No file uploaded in the request body. Please provide a base64-encoded file."}, status=400)

            # Check if file data was retrieved successfully
            if not file_data:
                return JsonResponse({"status": "error", "message": "No file provided. Please provide a base64-encoded file."}, status=400)

            if file_type.startswith('image'):
                file_type = 'image'
            elif file_type == 'application/pdf':
                file_type = 'pdf'
            else:
                return JsonResponse({"status": "error", "message": "Error File Format!! Please make sure files are image or pdf."}, status=400)

            # Now that we have the file_data and file_type, proceed with invoice extraction
            info_extractor = Invoice_Extractor()
            final_info = info_extractor.file_to_text_info(file_data, file_type)

            final_info_json = json.loads(final_info)  # Convert JSON string back to dictionary

            response_data = {"status": "success", "data": final_info_json}

            return JsonResponse(response_data, safe=False)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

