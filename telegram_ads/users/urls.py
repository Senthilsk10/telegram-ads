from django.urls import path
from .views import user_webhook


urlpatterns = [
    path("webhook",user_webhook,name="user_bot_path"),
]