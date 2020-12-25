from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from .models import Tweet

# Create your views here.

def home_view(request):
    return render(request, 'pages/home.html', context={}, status=200)

def tweet_detail_view(request, tweet_id,*args, **kwargs):
    # REST API
    # Format JSON
    data = {
        "id": tweet_id
    }
    status = 200
    try: 
        tweet = Tweet.objects.get(id=tweet_id)
    except:
        data['message'] = "Tweet not found."
        status = 404
    data['content'] = tweet.content
    return JsonResponse(data, status=status)