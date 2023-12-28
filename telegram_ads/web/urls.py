from django.urls import path
from .views import share_file_view

app_name = 'web'

urlpatterns = [
    path('share_file/<str:param>/', share_file_view, name='share_file'),
    
]
