# messaging/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import requests

class SendMessageView(View):
    def get(self, request):
        bot_token = 'YOUR_BOT_TOKEN'  # Replace with your bot token
        username = request.GET.get('username')  # Get the username from the query parameters
        message = request.GET.get('message')  # Get the message from the query parameters

        if not username:
            return JsonResponse({'error': 'Username is required.'}, status=400)
        
        if not message:
            return JsonResponse({'error': 'Message is required.'}, status=400)

        # Step 1: Get updates to find the chat_id
        updates_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
        updates_response = requests.get(updates_url)
        updates_data = updates_response.json()

        chat_id = None

        # Step 2: Loop through the updates to find the chat_id for the username
        for update in updates_data.get('result', []):
            message_data = update.get('message')
            if message_data:
                user = message_data.get('from')
                if user and user.get('username') == username:
                    chat_id = message_data['chat']['id']
                    break

        # If chat_id is found, send the message
        if chat_id:
            send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            payload = {
                'chat_id': chat_id,
                'text': message
            }
            response = requests.post(send_message_url, data=payload)
            return JsonResponse(response.json())
        else:
            return JsonResponse({'error': 'User has not interacted with the bot yet.'})

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')