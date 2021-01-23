from django.shortcuts import render
from django.http import JsonResponse, Http404

from .forms import TweetForm
from .models import Tweet

# Create your views here.


def home_view(request):
    return render(request, 'pages/home.html', context={}, status=200)


def tweet_create_view(request):
    form = TweetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = TweetForm()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
    if form.errors:
        return JsonResponse(form.errors, status=400)


def tweet_list_view(request):
    tweets = Tweet.objects.all()
    tweets_list = [tweet.serialize() for tweet in tweets]
    data = {
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    # REST API
    # Format JSON
    data = {
        "id": tweet_id
    }
    status = 200
    try:
        tweet = Tweet.objects.get(id=tweet_id)
    except Exception:
        data['message'] = "Tweet not found."
        status = 404
    data['content'] = tweet.content
    return JsonResponse(data, status=status)
