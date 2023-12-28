from django.urls import path
from .views import share_file_view,send_file,recieve_webhook

app_name = 'web'

urlpatterns = [
    path('share_file/<str:param>/', share_file_view, name='share_file'),
    path('send_file/<str:param>/',send_file,name = "send_file"),
    path('webhook',recieve_webhook,name='web_webhook')
]
