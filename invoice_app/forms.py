# # forms.py
# from django import forms
# class UploadFileForm(forms.Form):
#     file = forms.FileField(required=True)


#
from django import forms
from django.forms.widgets import ClearableFileInput


class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


class UploadFileForm(forms.Form):
    files = forms.FileField(widget=MultipleFileInput(attrs={'multiple': True}))
















