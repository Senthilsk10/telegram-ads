from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import get_object_or_404
import json,requests
from django.http import JsonResponse
from .models import client,File
from users.text_extraction import parse_file_details
from decimal import Decimal

#token fot tutorial bot - this bot's function is to recieve files from client and send it to the common group where the file sender is:
TOKEN = '6697337063:AAE5paU-w7wkdzmrbZCnVkTZpNu9wrlqTRY'
API_URL = f'https://api.telegram.org/bot{TOKEN}/'
@csrf_exempt
def client_webhook(request):
    try:
        
        update = json.loads(request.body)
        #print(update)
        message = update.get('message', {})
        user_id = message.get('from', {}).get('id')
        chat_type = message['chat']['type']
        if chat_type == 'group':
            send_response(message['chat']['id'],message['message_id'],'please dont message i am weak lmao')
            return JsonResponse('success',safe=False,status=200)
        elif client.objects.filter(client_id=user_id).exists():
            if 'document' in message:
                try:
                    #file_id = message['document']['file_id']
                    file_info = parse_file_details(message['caption'])
                    file_info['series_movie'] = file_info.pop('type')
                    file_info['file_id'] = message['document']['file_id']
                    file_info['file_size'] = kb_to_gb(message['document']['file_size'])
                    file_info['client'] = client.objects.get(client_id=user_id)
                    #print(file_info)
                    try:
                        #print(file_info)
                        new_file = File(**file_info)
                        new_file.save()
                        send_response(user_id, message['message_id'], "file added succesfully")
                        send_file_by_file_id(new_file.file_id,new_file.id)
                    
                    except:
                        send_response(user_id, message['message_id'], "could not save file details because of the data problems")
                except:
                    send_response(user_id, message['message_id'], "Format is wrong")


            elif message['text'] == '/upload_file':
                send_message_with_force_reply(user_id, "Please send the file in the appropriate format")
            else:
                
                send_response(user_id,message['message_id'],"Sorry i can't respond to that")

        else:
            if 'reply_to_message' in update['message']:
                original_message_text = update['message']['reply_to_message']['text']
                user_reply = update['message']['text']
                expected_prompt = 'enter your secret key from the portal'
                if original_message_text == expected_prompt:
                    if (client.objects.filter(client_key = user_reply)).exists():
                        user = client.objects.get(client_key = user_reply)
                        user.client_id = message['from']['id']
                        user.client_name = message['from']['username']
                        user.save()
                        send_response(message['chat']['id'],message['message_id'],"your account was connected you can now start sending messages")
                    else:
                        send_response(message['from']['id'],message['id'],"could not find your account")
                    #print(f"The user's reply '{user_reply}' is in response to the prompt '{expected_prompt}'")
                    # Perform additional actions based on the verification
                else:
                    print(f"The user's reply is not in response to the expected prompt")

                return JsonResponse("success", safe=False, status=200)

            elif message['text'] == "/connect_portal":
                print(message['text'])
                send_message_with_force_reply(message['chat']['id'], "enter your secret key from the portal")
            elif message['text'] == '/help':
                send_response(user_id, message.get('id'), "generate key from the website and access the key here and use it to verify your chat ID")
            else:
                send_response(user_id, message.get('id'), "sorry i cant respond to that")
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

class welcome(View):
    def get(self,request):
        template_name = 'welcome.html'
        API_KEY = request.user.client_key
        return render(request,template_name,{"apikey":API_KEY})

def send_message_with_force_reply(chat_id, message_text):
   

    # Set up the parameters for the sendMessage API method
    params = {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': {'force_reply': True}
    }

    # Make the request to the Telegram Bot API
    response = requests.post(API_URL+"sendMessage", json=params)

    # Process the JSON response
    if response.ok:
        result_json = response.json()
        if result_json['ok']:
            # Message sent successfully
            message_info = result_json['result']
            print("user is replying")
            #print(message_info['text'])
            #print(f"Message ID: {message_info['message_id']}")
        else:
            # Handle errors if needed
            print(f"Error: {result_json['description']}")
    else:
        # Handle HTTP request errors if needed
        print(f"HTTP Error: {response.status_code}")
        return "done"


def kb_to_gb(kb_size):
    gb_size = Decimal(kb_size)/Decimal(1024**3)
    return round(gb_size, 6)


def send_file_by_file_id(file_id,id):
    chat_id = -4016116094
    send_document_url = f'{API_URL}sendDocument'
    #print(chat_id,file_id)
    send_document_params = {
        'chat_id': chat_id,
        'caption':id,
        'document': file_id  # Use the file_id directly
    }

    send_document_response = requests.post(send_document_url, params=send_document_params)
    print(send_document_response.json())
    update = send_document_response.json()
    message = update['result']
    if 'document' in message:
        file_model_id = message.get('caption','')
        file_id = message['document']['file_id']
        file = File.objects.get(id=file_model_id)
        print(file.file_id)
        file.file_id = file_id
        file.save()
        print(file.file_id)
    if send_document_response.json().get('ok', False):
        print('File sent successfully!')
    else:
        print('Failed to send file.')