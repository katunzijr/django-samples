from django.urls import path, include
from .views import *

app_name = 'fileupload'
urlpatterns = [
    path('return/attachments/', MultipleFileUploadAPIView.as_view()),
    path('uploads/', htmlview, name='upload-files'),
]

