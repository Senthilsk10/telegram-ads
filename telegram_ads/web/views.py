from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Link_to_file
TOKEN ='6680854062:AAH5p2mhpEqpFLwC64s_Vy1qjwPgWRrYdK8'
API_URL = f'https://api.telegram.org/bot{TOKEN}/'

@csrf_exempt
def share_file_view(request, param):
    # Your view logic here
    return HttpResponse(f"This is the share_file view. Parameter received: {param}")


def send_file(request,param):
    try:
        file = File.objects.get(file_id=param)
        chat_id = file.user_chat_id
        send_file_by_file_id(chat_id,file.file_id)
        

def send_file_by_file_id(chat_id, file_id):
    send_document_url = f'{APIURL}+sendDocument'
    send_document_params = {
        'chat_id': chat_id,
        'caption':"some xxx",
        'document': file_id  # Use the file_id directly
    }
    
    send_document_response = requests.post(send_document_url, params=send_document_params)

    if send_document_response.json().get('ok', False):
        print('File sent successfully!')
    else:
        print('Failed to send file.')
  
