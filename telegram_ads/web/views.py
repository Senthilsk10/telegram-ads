from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from .models import Link_to_file
from client.models import File,verified_groups
from django.urls import reverse_lazy
import requests,json

TOKEN ='6680854062:AAH5p2mhpEqpFLwC64s_Vy1qjwPgWRrYdK8'
API_URL = f'https://api.telegram.org/bot{TOKEN}/'


@csrf_exempt
def recieve_webhook(request):

    update = json.loads(request.body)
    #print(update)
    if 'message' in update:
        message = update.get('message',{})
        print(message)
    else:
        message = update.get('result',{})
        print(message)
    chat_id = message['chat']['id']
    message_id = message['message_id']
    chat_type = message['chat']['type']
    if chat_type == 'group':
        if 'document' in message:
            file_model_id = message.get('caption','')
            file_id = message['document']['file_id']
            file = File.objects.get(id=file_model_id)
            print(file.file_id)
            file.file_id = file_id
            file.save()
            print(file.file_id)
            return JsonResponse('success',safe=False,status=200)
            #send_response(chat_id,message_id,f"the file id for telegram is {file_id}, for model is {file_model_id}")
        else:
            print('here')
            send_response(chat_id,message_id,"please send files only")
            return JsonResponse('success',safe=False,status=200)
    else:
        send_response(chat_id,message_id," sorry i can't do that i can only send files")
        return JsonResponse('success',safe=False,status=200)
    return JsonResponse('success',safe=False,status=200)
    
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
        caption = file.description()
        try:
            send_file_by_file_id(chat_id,caption,file.file_id)
        except:
            print('failed to send')
            return JsonResponse('success',safe=False,status=200)
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
    


def send_file_by_file_id(chat_id,caption,file_id):
    send_document_url = f'{API_URL}sendDocument'
    print(chat_id,file_id)
    send_document_params = {
        'chat_id': chat_id,
        'caption':caption,
        'document': file_id  # Use the file_id directly
    }

    send_document_response = requests.post(send_document_url, params=send_document_params)
    print(send_document_response.json())
    if send_document_response.json().get('ok', False):
        print('File sent successfully!')
    else:
        raise ValueError('Failed to send file.')

def send_response(chat_id, message_id,text):
    response_url = API_URL + f'sendMessage?chat_id={chat_id}&text={text}&reply_to_message_id={message_id}'
    response = requests.get(response_url)

    if response.status_code == 200:
        print("Response sent successfully")
    else:
        print("Error sending response:", response.text)
