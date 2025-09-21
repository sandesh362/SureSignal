# text_processing/tasks.py (Celery tasks for async processing)
from celery import shared_task
from .services import TextCleaningService
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_tweets_task(limit=None):
    """Async task to process tweet text"""
    cleaning_service = TextCleaningService()
    processed_count = cleaning_service.process_tweets(limit=limit)
    logger.info(f"Tweet processing task completed: {processed_count} tweets processed")
    return {'processed_count': processed_count}

@shared_task
def process_articles_task(limit=None):
    """Async task to process article text"""
    cleaning_service = TextCleaningService()
    processed_count = cleaning_service.process_articles(limit=limit)
    logger.info(f"Article processing task completed: {processed_count} articles processed")
    return {'processed_count': processed_count}

@shared_task
def process_all_task(tweet_limit=None, article_limit=None):
    """Async task to process all text"""
    cleaning_service = TextCleaningService()
    result = cleaning_service.process_all(
        tweet_limit=tweet_limit, 
        article_limit=article_limit
    )
    logger.info(f"All text processing task completed: {result}")
    return result

@shared_task
def scheduled_text_processing():
    """Scheduled task to process text periodically"""
    logger.info("Starting scheduled text processing...")
    
    # Process tweets
    tweets_result = process_tweets_task.delay()
    
    # Process articles
    articles_result = process_articles_task.delay()
    
    return {
        'tweets_task_id': tweets_result.id,
        'articles_task_id': articles_result.id
    }