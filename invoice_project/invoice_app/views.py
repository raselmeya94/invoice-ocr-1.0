# views.py
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .utils import extract_text_from_file , information_retrieve
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
import pandas as pd




def upload_file(request):
    # print("Output: " , request.FILES.getlist('files'))
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
                print("something")
                # return render(request, 'index.html', {
                #     'form': form,
                #     'error': 'Unsupported file type for: {}'.format(uploaded_file.name)
                # })
            #
            extracted_text = extract_text_from_file(file_data, file_type)
            encoded_file = base64.b64encode(file_data).decode('utf-8')
            # Generate DataFrame and HTML for each file
            df = information_retrieve(extracted_text)
            df_html = df.to_html(index=False)
            # print(uploaded_file.size)

            data.append({
                'filename': uploaded_file.name,
                'file_size': str(round(uploaded_file.size / 1024 , 2))+" KB",
                'uploaded_file_data':encoded_file,
                'extracted_text': extracted_text,
                'file_type': file_type,
                'df_html': df_html,
            })
            # data.append({
            #     uploaded_file.name: {
            #         'uploaded_file_data': encoded_file,
            #         'extracted_text': extracted_text,
            #         'file_type': file_type,
            #         'df_html': None
            #     }
            # })
        print((len(data)))


        return render(request, 'index.html', {'form': form, 'data': data })


    else:
        form = UploadFileForm()
        return render(request, 'index.html', {'form': form, })





