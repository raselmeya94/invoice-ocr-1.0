# views.py
from django.shortcuts import render
from .forms import UploadImageForm
from .utils import extract_text_from_image  # Assuming you have a utility function for text extraction
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image: InMemoryUploadedFile = form.cleaned_data['image']
            
            # Read the file in memory
            image_data = image.read()

            # Extract text from the image
            extracted_text = extract_text_from_image(image_data)

            # Encode the image data to base64
            encoded_image = base64.b64encode(image_data).decode('utf-8')

            # Return the uploaded image and extracted text in the response
            return render(request, 'index.html', {
                'form': form,
                'uploaded_image_data': encoded_image,
                'uploaded_image_name': image.name,
                'extracted_text': extracted_text
            })
    else:
        form = UploadImageForm()
    return render(request, 'index.html', {'form': form})
