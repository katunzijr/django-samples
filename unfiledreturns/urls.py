from django.urls import path
from .views import *

app_name = 'unfiledreturns'
urlpatterns = [
    path('monthly/', UnfiledReturnMonthlyAPIView.as_view(), name='monthly'),
    path('annually/', UnfiledReturnMonthlyAPIView.as_view(), name='annually'),
]
