from django.urls import path
from .views import client_webhook


urlpatterns = [
    path("webhook",client_webhook,name="client_bot_path")
]