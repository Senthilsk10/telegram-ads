from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import get_object_or_404
import json,requests
from django.http import JsonResponse
from .models import client
import secrets
from django.conf import settings



TOKEN = '6697337063:AAE5paU-w7wkdzmrbZCnVkTZpNu9wrlqTRY'
API_URL = f'https://api.telegram.org/bot{TOKEN}/'
@csrf_exempt
def client_webhook(request):
    try:
        update = json.loads(request.body)
        print(update)
        message = update.get('message', {})
        callback_query = update.get('callback_query', {})
        user_id = message.get('from', {}).get('id')
        
        if Client.objects.filter(client_id=user_id).exists():
            print("user present")
        else:
            send_response(user_id, message.get('id'), "generate key from the website and access the key here and use it to verify your chat ID")
            return JsonResponse("success", safe=False, status=200)
        
        
        return JsonResponse("success",safe=False,status = 200)
    
    
    except Exception as e:
        print(e)
        return JsonResponse("success",safe=False,status = 200)




def send_response(chat_id, message_id,text):
    response_url = API_URL + f'sendMessage?chat_id={chat_id}&text={text}&reply_to_message_id={message_id}'
    response = requests.get(response_url)

    if response.status_code == 200:
        print("Response sent successfully")
    else:
        print("Error sending response:", response.text)


class login(LoginView):
    success_url = reverse_lazy("welcome")



def generate_random_string(length=50):
    return secrets.token_urlsafe(length)

SECRET_KEY = settings.SECRET_KEY
class welcome(View):
    def get(self,request):
        template_name = 'welcome.html'
        API_KEY = generate_random_string() + SECRET_KEY
        return render(request,template_name,{"apikey":API_KEY})





