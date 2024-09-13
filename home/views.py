from django.shortcuts import render,  redirect
from .forms import feedback_form, contact_form
from .models import feedback

import requests
import xml.etree.ElementTree as ET

def fetch_rss_stories(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch RSS feed. Status code: {response.status_code}")
        return None

    # Parse the RSS feed
    root = ET.fromstring(response.content)
    
    # Extract all <item> elements from the RSS feed
    stories = []
    for item in root.findall('.//item'):
        # Get the description
        description = item.find('description').text if item.find('description') is not None else "No description"
        
        # Get the image URL
        media_content = item.find('{http://search.yahoo.com/mrss/}content')
        image_url = media_content.get('url') if media_content is not None else "No image"
        
        # Get the topic (title)
        topic = item.find('title').text if item.find('title') is not None else "No title"

        link = item.find('link').text if item.find('link') is not None else "No link"
        # Append the story as a dictionary
        stories.append({
            'topic': topic,
            'description': description,
            'image': image_url,
            'link': link
        })
    
    return stories

rss_url = "https://feeds.content.dowjones.io/public/rss/mw_topstories"






# Create your views here
def home(request):
    if request.method == 'POST':
        text = request.POST['text']
        return redirect(f'/assistant/message/{text}')
    
    stories = fetch_rss_stories(rss_url)
    feed = feedback.objects.all()
    context = {
        'stories' : stories,
        'feedback' : feed
    }
    return render(request, 'home.html', context=context)

from django.contrib.auth.decorators import login_required

@login_required(login_url='/user/login')
def feedback_form_view(request):
    if request.method == 'POST':
        form = feedback_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    form = feedback_form()
    return render(request, 'feedback.html', context={'form': form})


@login_required(login_url='/user/login')
def contact_us(request):
    if request.method == 'POST':
        form = contact_form(request.POST)
        form.user = request.user
        if form.is_valid():
            contact_message = form.save(commit=False)  # Create an instance without saving
            contact_message.user = request.user  # Assign the user
            contact_message.save()
            return redirect('/')
    
    form = contact_form()
    context = {
        'form' : form
    }
    return render(request, 'contact.html', context=context)
    

def about_us(request):
    return render(request, 'about.html')