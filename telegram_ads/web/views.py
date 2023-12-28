from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from .models import Link_to_file
from client.models import File,verified_groups
from django.urls import reverse_lazy
import requests,json

TOKEN ='6697337063:AAE5paU-w7wkdzmrbZCnVkTZpNu9wrlqTRY'
API_URL = f'https://api.telegram.org/bot{TOKEN}/'


@csrf_exempt
def recieve_webhook(request):
    update = request.body()
    chat_id = update['message']['chat']['id']
    send_response(chat_id,"i can't do that")

@csrf_exempt
def share_file_view(request, param):
    alive = Link_to_file.objects.filter(param=param).exists()
    if alive:
        url = reverse_lazy('web:send_file',kwargs = {'param':param})
        target_url = f"https://stunning-space-tribble-5w5xx46q4qwfwx9-8000.preview.app.github.dev/{url}"

        response_content = f"<html><body>This is the share_file view. Click this link to get your file: <a href='{target_url}'>click here</a></body></html>"

        return HttpResponse(response_content)
    else:
        response_content = f"<html><body><h3>vell apoda poolu</h3></body></html>"
        return HttpResponse(response_content)

@csrf_exempt
def send_file(request,param):
    try:
        link_instance = Link_to_file.objects.get(param=param)
        file = link_instance.file
        chat_id = link_instance.user_chat_id
        send_file_by_file_id(TOKEN,chat_id,file.file_id)
        group = link_instance.group_id
        count_g = group.forwardedcount_for_group
        count_g +=1
        group.forwardedcount_for_group = count_g
        count_f = file.Forwarded_count
        count_f += 1
        file.Forwarded_count = count_f
        file.save()
        group.save()
        link_instance.is_shared = True
        link_instance.save()
    except Exception as e:
        return JsonResponse(f'not ok {e}',safe=False,status=400)
    return JsonResponse('ok',safe=False,status=200)
    


def send_file_by_file_id(bot_token, chat_id, file_id):
    # Step 1: Send the file using sendDocument method
    send_document_url = f'https://api.telegram.org/bot{bot_token}/sendDocument'
    send_document_params = {
        'chat_id': chat_id,
        'caption':"some xxx",
        'document': file_id  # Use the file_id directly
    }

    send_document_response = requests.post(send_document_url, params=send_document_params)
    print(send_document_response.json())
    if send_document_response.json().get('ok', False):
        print('File sent successfully!')
    else:
        print('Failed to send file.')




def send_response(chat_id,text):
    response_url = API_URL + f'sendMessage?chat_id={chat_id}&text={text}'
    response = requests.get(response_url)

    if response.status_code == 200:
        print("Response sent successfully")
    else:
        print("Error sending response:", response.text)
