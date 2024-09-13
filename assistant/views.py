from django.shortcuts import render, HttpResponse, redirect
import requests
from .models import sessions
from website.settings import API_KEY_ONDEMAND, CLIENT_KEY_ONDEMAND

api_key = API_KEY_ONDEMAND
external_user_id = CLIENT_KEY_ONDEMAND

def new_session():
    create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
    create_session_headers = {
        'apikey': api_key
    }
    create_session_body = {
        'pluginIds': [],
        'externalUserId': external_user_id
    }
    response = requests.post(create_session_url, headers=create_session_headers, json=create_session_body)
    response_data = response.json()
    session_id = response_data['data']['id']
    return session_id

def get_chat(session_id, query : str):
    submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
    submit_query_headers = {
        'apikey': api_key
    }
    submit_query_body = {
        'endpointId': 'predefined-openai-gpt4o',
        'query': query,
        'pluginIds': ['plugin-1712327325', 'plugin-1713962163', 'plugin-1726234847'],
        'responseMode': 'sync'
    }

    response = requests.post(submit_query_url, headers=submit_query_headers, json=submit_query_body)
    query_response_data = response.json()

    
    return str(query_response_data['data']['answer'])






import requests

def fetch_chat_details(session_id):
    url = f"https://api.on-demand.io/chat/v1/sessions/{session_id}/messages"

    headers = {
        "accept": "application/json",
        "apikey": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_response = response.json()
        chat_details = []

        # Loop through each message in the data
        for message in json_response.get("data", []):
            # Extract the query (question), answer, and the createdAt date
            chat_info = {
                "question": message.get("query"),
                "answer": message.get("answer"),
                "date": message.get("createdAt")
            }
            chat_details.append(chat_info)

        return chat_details
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


from django.contrib.auth.decorators import login_required




@login_required(login_url='/user/login')
def assistant(request, query='what can you do'):
    if request.method == 'POST':
        text = request.POST['text']
        return redirect(f'/assistant/message/{text}')

    session = sessions.objects.filter(user=request.user)
    if session.exists():
        details = fetch_chat_details(str(session.first().session_id))
        data = get_chat(session.first().session_id, query)
    else:
        details = ''
        session = new_session()
        save = sessions(user=request.user, session_id = session)
        save.save()
        data = get_chat(session, query)
    
    context = {
        'details' : details,
        'data' : str(data)
    }
    
    return render(request, 'chat.html', context=context)

@login_required(login_url='/user/login')
def clear_session(request):
    session = sessions.objects.filter(user=request.user)
    if session.exists():
        session.delete()
        return redirect('/')
    else:
        return redirect('/')
