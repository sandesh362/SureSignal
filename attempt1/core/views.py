from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tweet, NewsArticle
from .serializers import TweetSerializer, NewsArticleSerializer
from .database import db_manager

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_tweets = Tweet.objects.count()
        processed_tweets = Tweet.objects.exclude(cleaned_text__isnull=True).count()
        
        return Response({
            'total_tweets': total_tweets,
            'processed_tweets': processed_tweets,
            'unprocessed_tweets': total_tweets - processed_tweets
        })

class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_articles = NewsArticle.objects.count()
        processed_articles = NewsArticle.objects.exclude(cleaned_text__isnull=True).count()
        
        return Response({
            'total_articles': total_articles,
            'processed_articles': processed_articles,
            'unprocessed_articles': total_articles - processed_articles
        })

def dashboard(request):
    """Main dashboard view"""
    context = {
        'total_tweets': Tweet.objects.count(),
        'total_articles': NewsArticle.objects.count(),
        'processed_tweets': Tweet.objects.exclude(cleaned_text__isnull=True).count(),
        'processed_articles': NewsArticle.objects.exclude(cleaned_text__isnull=True).count(),
    }
    return render(request, 'core/dashboard.html', context)

def api_status(request):
    """API status endpoint"""
    return JsonResponse({
        'status': 'ok',
        'database_connected': db_manager.connected,
        'total_tweets': Tweet.objects.count(),
        'total_articles': NewsArticle.objects.count(),
    })

# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('tweets', views.TweetViewSet)
router.register('articles', views.NewsArticleViewSet)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/status/', views.api_status, name='api_status'),
    path('api/', include(router.urls)),
]

# core/admin.py
from django.contrib import admin
from .models import Tweet, NewsArticle

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('tweet_id', 'author_id', 'created_at', 'lang', 'text_preview')
    list_filter = ('lang', 'created_at', 'platform')
    search_fields = ('tweet_id', 'text', 'author_id')
    readonly_fields = ('processed_at',)
    
    def text_preview(self, obj):
        return obj.text[:100] + "..." if len(obj.text) > 100 else obj.text
    text_preview.short_description = 'Text Preview'

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title_preview', 'source', 'author', 'published_at')
    list_filter = ('source', 'published_at', 'platform')
    search_fields = ('title', 'description', 'author', 'source')
    readonly_fields = ('processed_at',)
    
    def title_preview(self, obj):
        return obj.title[:100] + "..." if len(obj.title) > 100 else obj.title
    title_preview.short_description = 'Title'