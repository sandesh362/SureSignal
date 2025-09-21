from django.urls import path
from . import views

urlpatterns = [
    path('', views.processing_dashboard, name='processing_dashboard'),
    path('tweets/', views.process_tweets, name='process_tweets'),
    path('articles/', views.process_articles, name='process_articles'),
    path('all/', views.process_all_text, name='process_all_text'),
    path('stats/', views.processing_stats, name='processing_stats'),
]