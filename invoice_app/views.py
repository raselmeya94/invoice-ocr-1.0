# views.py
from django.shortcuts import render
from .forms import UploadFileForm
from .utils import extract_text_from_file
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file: InMemoryUploadedFile = form.cleaned_data['file']
            
            # Read the file in memory
            file_data = uploaded_file.read()
            file_type = uploaded_file.content_type
            
            # Determine the file type (image or PDF)
            if file_type.startswith('image'):
                file_type = 'image'
            elif file_type == 'application/pdf':
                file_type = 'pdf'
            else:
                return render(request, 'index.html', {
                    'form': form,
                    'error': 'Unsupported file type.'
                })

            # Extract text from the file
            extracted_text = extract_text_from_file(file_data, file_type)

            # Encode the file data to base64 for display
            encoded_file = base64.b64encode(file_data).decode('utf-8')

            # Return the uploaded file and extracted text in the response
            return render(request, 'index.html', {
                'form': form,
                'uploaded_file_data': encoded_file,
                'uploaded_file_name': uploaded_file.name,
                'extracted_text': extracted_text,
                'file_type': file_type
            })
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})
