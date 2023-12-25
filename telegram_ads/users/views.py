from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import requests
from .text_extraction import parse_file_details


TOKEN = '6785780878:AAEGtVwuH-ITvBGkd2SzPz7KGsUzsu_loVU'
API_URL = f'https://api.telegram.org/bot{TOKEN}/'


@csrf_exempt
def user_webhook(request):
    update = json.loads(request.body)
    callback_query = update.get('callback_query',{})
    message = update.get('message', {})
    chat = message.get('chat', {})
    print(update)
    movie_text = parse_file_details(message['text'])
    send_response(chat['id'],message['message_id'],f'you asked for the movie :{movie_text}')
    return JsonResponse("success", safe=False, status=200)




def send_response(chat_id, message_id,text):
    response_url = API_URL + f'sendMessage?chat_id={chat_id}&text={text}&reply_to_message_id={message_id}'
    response = requests.get(response_url)

    if response.status_code == 200:
        print("Response sent successfully")
    else:
        print("Error sending response:", response.text)


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



def select_file(chat_id, options):
    keyboard = {
        'inline_keyboard': [
            [{'text': text, 'callback_data': text}] for text in options
        ]
    }

    reply_markup = json.dumps(keyboard)

    message = 'Here are your links:'
    send_message_url = TELEGRAM_API_URL + f'sendMessage?chat_id={chat_id}&text={message}&reply_markup={reply_markup}'

    response = requests.get(send_message_url)

    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Error sending message:", response.text)
    