from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND
)

from tweets.forms import TweetForm
from tweets.models import Tweet
from tweets.serializer import TweetSerializer, TweetActionSerializer

# Create your views here.


def home_view(request):
    return render(request, 'pages/home.html', context={}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_create_view(request):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=HTTP_201_CREATED)
    return Response({}, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def tweet_list_view(request):
    tweets = Tweet.objects.all()
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs:
        return Response({}, status=HTTP_404_NOT_FOUND)
    tweet = qs.first()
    serilizer = TweetSerializer(tweet)
    return Response(serilizer.data, status=HTTP_200_OK)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    tweets = Tweet.objects.filter(id=tweet_id)
    if not tweets.exists():
        return Response({}, status=HTTP_404_NOT_FOUND)
    tweet = tweets.filter(user=request.user)
    if not tweet.exists():
        return Response(
            {"message": "You cannot delete this tweet"},
            status=HTTP_403_FORBIDDEN
        )
    tweet.delete()
    return Response({"message": "Tweet has been deleted"}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")

        tweets = Tweet.objects.filter(id=tweet_id)
        if not tweets.exists():
            return Response({}, status=HTTP_404_NOT_FOUND)
        tweet = tweets.first()
        if action == 'like':
            tweet.likes.add(request.user)
            obj = TweetSerializer(tweet)
            return Response(obj.data, status=HTTP_200_OK)
        elif action == 'unlike':
            tweet.likes.remove(request.user)
        elif action == 'retweet':
            pass
    return Response({}, status=HTTP_200_OK)


def tweet_create_view_pure_django(request):
    user = request.user
    if not request.user.is_authenticated:
        request.user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
    form = TweetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        form = TweetForm()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
    if form.errors:
        return JsonResponse(form.errors, status=400)


def tweet_list_view_pure_django(request):
    tweets = Tweet.objects.all()
    tweets_list = [tweet.serialize() for tweet in tweets]
    data = {
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
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
