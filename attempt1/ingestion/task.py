from celery import shared_task
from .services import TwitterService, NewsService
import logging

logger = logging.getLogger(__name__)

@shared_task
def collect_tweets_task(query="misinformation OR fake news", max_results=10):
    """Async task to collect tweets"""
    twitter_service = TwitterService()
    result = twitter_service.collect_tweets(query=query, max_results=max_results)
    logger.info(f"Tweet collection task completed: {result}")
    return result

@shared_task
def collect_news_task(query="misinformation OR fake news", page_size=5):
    """Async task to collect news"""
    news_service = NewsService()
    result = news_service.collect_news(query=query, page_size=page_size)
    logger.info(f"News collection task completed: {result}")
    return result

@shared_task
def scheduled_data_collection():
    """Scheduled task to collect data periodically"""
    logger.info("Starting scheduled data collection...")
    
    # Collect tweets
    tweets_result = collect_tweets_task.delay()
    
    # Collect news
    news_result = collect_news_task.delay()
    
    return {
        'tweets_task_id': tweets_result.id,
        'news_task_id': news_result.id
    }
