from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import requests
from .text_extraction import parse_file_details
from client.models import File,client,verified_groups
from django.db.models import Q
from web.models import Link_to_file


#token for file_Filter_sender - this bot will be used for sending initial filtered files and link for user , better send the link too to the user chat so we can try to reduce the messages in the group 
TOKEN = '6785780878:AAEGtVwuH-ITvBGkd2SzPz7KGsUzsu_loVU'
API_URL = f'https://api.telegram.org/bot{TOKEN}/'


@csrf_exempt
def user_webhook(request):
    update = json.loads(request.body)
    callback_query = update.get('callback_query',{})
    message = update.get('message', {})
    chat = message.get('chat', {})
    print(update)
    if chat['type'] == 'group':
        send_response(chat['id'],message['message_id'],'this is a group which is not registered')
        return JsonResponse('ok',safe=False,status=200)
    if callback_query:
        file_id = callback_query['data']
        user_id = callback_query['from']['id']
        group_id = callback_query['message']['chat']['id']
        try:
            file = File.objects.get(id=file_id)
        except:
            send_response(group_id,callback_query['message']['message_id'],'file has been deleted')
            return JsonResponse('success',safe=False,status=200)
        group = verified_groups.objects.get(group_id=group_id)
        link = Link_to_file.objects.create(file = file,group_id = group,user_chat_id = user_id)
        url = link.get_link()
        send_response(group_id,callback_query['message']['message_id'],f"here is your link - {url}")


    elif message:

        try:
            data_dict = parse_file_details(message['text'])
            if 'movie' or 'series' not in data_dict:
                send_response(chat['id'],message['message_id'],f'No results Found - Try to send in correct format')
                return JsonResponse('success',safe=False,status=200)
            query = Q()

            if 'file_name' in data_dict:
                query &= Q(file_name__icontains=data_dict['file_name'])

            if 'year' in data_dict:
                query &= Q(year=int(data_dict['year']))

            if 'quality' in data_dict:
                query &= Q(quality=data_dict['quality'])
            
            if 'language' in data_dict:
                query &= Q(language=data_dict['language'])
            
            if 'season' in data_dict:
                query &= Q(season=data_dict['season'])
            
            if 'episode' in data_dict:
                query &= Q(episode=data_dict['episode'])
            try:
                result = File.objects.filter(query)
            except:
                send_response(chat['id'],message['message_id'],'no files found for your search text')
                return JsonResponse('success',safe=False,status=200)
            send_response(chat['id'],message['message_id'],f'you asked for the movies:{result}')
            select_file(chat['id'],result)
        except Exception as e:
            print(e)
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
            [{'text': f'{item.file_size} GB  {item.file_name} {item.year if item.year else " "} { item.season,item.episode if item.season and item.episode else item.language,item.quality}', 'callback_data':item.id}] for item in options
        ]
    }

    reply_markup = json.dumps(keyboard)

    message = 'Here are your links:'
    send_message_url = API_URL + f'sendMessage?chat_id={chat_id}&text={message}&reply_markup={reply_markup}'
    
    response = requests.get(send_message_url)

    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Error sending message:", response.text)
    