# invoice_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='index'),
    path('api/invoice_info/', views.invoice_information, name='invoice_info'),
]
