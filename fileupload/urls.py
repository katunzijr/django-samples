from django.urls import path, include
from .views import *

app_name = 'fileupload'
urlpatterns = [
    # path('upload/', FileUploadAPIView.as_view(), name='upload-file'),
    path('return/attachments/', MultipleFileUploadAPIView.as_view()),
    path('uploads/', htmlview, name='upload-files'),
]

