from django.urls import path
from .views import client_webhook,login,welcome


urlpatterns = [
    path("webhook",client_webhook,name="client_bot_path"),
    path('login/', login.as_view(), name='login'),
    path('welcome/',welcome.as_view(),name = "welcome"),
]