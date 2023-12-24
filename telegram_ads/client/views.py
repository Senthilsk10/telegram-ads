from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse




TOKEN = '6697337063:AAE5paU-w7wkdzmrbZCnVkTZpNu9wrlqTRY'
API_URL = f'https://api.telegram.org/bot{TOKEN}/'
@csrf_exempt
def client_webhook(request):
    try:
        update = json.loads(request.body)
        print(update)
        return JsonResponse("success",safe=False,status = 200)
    except Exception as e:
        print(e)
        return JsonResponse("success",safe=False,status = 200)
