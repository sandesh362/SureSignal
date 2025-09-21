from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render
from .services import TwitterService, NewsService
from .tasks import collect_tweets_task, collect_news_task

@api_view(['POST'])
def collect_tweets(request):
    """Endpoint to trigger tweet collection"""
    query = request.data.get('query', 'misinformation OR fake news')
    max_results = request.data.get('max_results', 10)
    
    # Run synchronously for now, can be made async with Celery
    twitter_service = TwitterService()
    result = twitter_service.collect_tweets(query=query, max_results=max_results)
    
    if 'error' in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
def collect_news(request):
    """Endpoint to trigger news collection"""
    query = request.data.get('query', 'misinformation OR fake news')
    page_size = request.data.get('page_size', 5)
    
    # Run synchronously for now, can be made async with Celery
    news_service = NewsService()
    result = news_service.collect_news(query=query, page_size=page_size)
    
    if 'error' in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
def collect_all_data(request):
    """Endpoint to trigger both tweet and news collection"""
    query = request.data.get('query', 'misinformation OR fake news')
    max_results = request.data.get('max_results', 10)
    page_size = request.data.get('page_size', 5)
    
    twitter_service = TwitterService()
    news_service = NewsService()
    
    # Collect tweets
    tweets_result = twitter_service.collect_tweets(query=query, max_results=max_results)
    
    # Collect news
    news_result = news_service.collect_news(query=query, page_size=page_size)
    
    return Response({
        'tweets': tweets_result,
        'news': news_result
    }, status=status.HTTP_200_OK)

def ingestion_dashboard(request):
    """Dashboard for data ingestion"""
    context = {
        'twitter_configured': TwitterService().client is not None,
        'news_configured': NewsService().client is not None,
    }
    return render(request, 'data_ingestion/dashboard.html', context)