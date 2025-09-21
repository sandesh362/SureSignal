# text_processing/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render
from .services import TextCleaningService
from .tasks import process_tweets_task, process_articles_task, process_all_task
from core.models import Tweet, NewsArticle

@api_view(['POST'])
def process_tweets(request):
    """Endpoint to trigger tweet text processing"""
    limit = request.data.get('limit', None)
    
    cleaning_service = TextCleaningService()
    processed_count = cleaning_service.process_tweets(limit=limit)
    
    return Response({
        'success': True,
        'processed_count': processed_count
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def process_articles(request):
    """Endpoint to trigger article text processing"""
    limit = request.data.get('limit', None)
    
    cleaning_service = TextCleaningService()
    processed_count = cleaning_service.process_articles(limit=limit)
    
    return Response({
        'success': True,
        'processed_count': processed_count
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def process_all_text(request):
    """Endpoint to trigger processing of all unprocessed text"""
    tweet_limit = request.data.get('tweet_limit', None)
    article_limit = request.data.get('article_limit', None)
    
    cleaning_service = TextCleaningService()
    result = cleaning_service.process_all(
        tweet_limit=tweet_limit, 
        article_limit=article_limit
    )
    
    return Response({
        'success': True,
        **result
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def processing_stats(request):
    """Get text processing statistics"""
    total_tweets = Tweet.objects.count()
    processed_tweets = Tweet.objects.exclude(cleaned_text__isnull=True).count()
    unprocessed_tweets = total_tweets - processed_tweets
    
    total_articles = NewsArticle.objects.count()
    processed_articles = NewsArticle.objects.exclude(cleaned_text__isnull=True).count()
    unprocessed_articles = total_articles - processed_articles
    
    return Response({
        'tweets': {
            'total': total_tweets,
            'processed': processed_tweets,
            'unprocessed': unprocessed_tweets
        },
        'articles': {
            'total': total_articles,
            'processed': processed_articles,
            'unprocessed': unprocessed_articles
        },
        'overall': {
            'total': total_tweets + total_articles,
            'processed': processed_tweets + processed_articles,
            'unprocessed': unprocessed_tweets + unprocessed_articles
        }
    })

def processing_dashboard(request):
    """Dashboard for text processing"""
    # Get processing statistics
    total_tweets = Tweet.objects.count()
    processed_tweets = Tweet.objects.exclude(cleaned_text__isnull=True).count()
    
    total_articles = NewsArticle.objects.count()
    processed_articles = NewsArticle.objects.exclude(cleaned_text__isnull=True).count()
    
    context = {
        'spacy_available': SPACY_AVAILABLE,
        'total_tweets': total_tweets,
        'processed_tweets': processed_tweets,
        'unprocessed_tweets': total_tweets - processed_tweets,
        'total_articles': total_articles,
        'processed_articles': processed_articles,
        'unprocessed_articles': total_articles - processed_articles,
    }
    return render(request, 'text_processing/dashboard.html', context)
