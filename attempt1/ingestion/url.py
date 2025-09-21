from django.urls import path
from . import views

urlpatterns = [
    path('', views.ingestion_dashboard, name='ingestion_dashboard'),
    path('tweets/', views.collect_tweets, name='collect_tweets'),
    path('news/', views.collect_news, name='collect_news'),
    path('all/', views.collect_all_data, name='collect_all_data'),
]