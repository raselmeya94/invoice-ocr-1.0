from django.db import models

# Create your models here.
from django import forms
class UploadFileForm(forms.Form):
    file = forms.FileField()
