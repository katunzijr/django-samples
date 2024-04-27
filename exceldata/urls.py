from django.urls import path, include
from .views import *

app_name = 'fileupload'
urlpatterns = [
    path('upload-api/', ExcelFileUpload.as_view(), name='upload-api-files'),
    path('upload/', upload, name='upload-files'),
]
