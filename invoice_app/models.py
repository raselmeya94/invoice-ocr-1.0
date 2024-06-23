# from django.db import models

# Create your models here.
from django import forms
class UploadFileForm(forms.Form):
    file = forms.FileField()






# from django.db import models
#
# class UploadedFile(models.Model):
#     file = models.FileField(upload_to='uploads/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)