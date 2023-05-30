import openai
from django.http import JsonResponse
from django.shortcuts import render

from site_settings.models import Tokens

# get key from https://platform.openai.com/account/api-keys
openai.api_key = getattr(Tokens.objects.first(), 'openai')

# api documentation for chat: https://platform.openai.com/docs/guides/chat
def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    answer = response.choices[0].message.content.strip()
    return answer

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')
