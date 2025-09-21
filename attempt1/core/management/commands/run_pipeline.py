
# core/management/commands/run_pipeline.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from data_ingestion.services import TwitterService, NewsService
from text_processing.services import TextCleaningService
from core.models import Tweet, NewsArticle
import time

class Command(BaseCommand):
    help = 'Run the complete misinformation detection pipeline'

    def add_arguments(self, parser):
        parser.add_argument('--query', type=str, default='misinformation OR fake news',
                          help='Search query for data collection')
        parser.add_argument('--tweets', type=int, default=10,
                          help='Number of tweets to collect')
        parser.add_argument('--news', type=int, default=5,
                          help='Number of news articles to collect')
        parser.add_argument('--skip-collection', action='store_true',
                          help='Skip data collection phase')
        parser.add_argument('--skip-processing', action='store_true',
                          help='Skip text processing phase')
        parser.add_argument('--async', action='store_true',
                          help='Run tasks asynchronously using Celery')

    def handle(self, *args, **options):
        start_time = time.time()
        
        self.stdout.write(
            self.style.SUCCESS('🚀 Misinformation Detection Pipeline Starting...')
        )
        
        # Phase 1: Data Collection
        if not options['skip_collection']:
            self.stdout.write('\n📊 Starting data collection...')
            
            if options['async']:
                self.run_collection_async(options)
            else:
                self.run_collection_sync(options)
        
        # Phase 2: Text Processing
        if not options['skip_processing']:
            self.stdout.write('\n🔄 Starting text preprocessing...')
            
            if options['async']:
                self.run_processing_async()
            else:
                self.run_processing_sync()
        
        # Summary
        self.print_summary()
        
        end_time = time.time()
        duration = end_time - start_time
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Pipeline completed in {duration:.2f} seconds!')
        )

    def run_collection_sync(self, options):
        """Run data collection synchronously"""
        query = options['query']
        max_tweets = options['tweets']
        max_news = options['news']
        
        # Collect tweets
        twitter_service = TwitterService()
        tweets_result = twitter_service.collect_tweets(
            query=query, 
            max_results=max_tweets
        )
        
        if 'error' in tweets_result:
            self.stdout.write(
                self.style.ERROR(f"❌ Twitter collection failed: {tweets_result['error']}")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Collected {tweets_result['inserted']} tweets")
            )
        
        # Collect news
        news_service = NewsService()
        news_result = news_service.collect_news(
            query=query, 
            page_size=max_news
        )
        
        if 'error' in news_result:
            self.stdout.write(
                self.style.ERROR(f"❌ News collection failed: {news_result['error']}")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Collected {news_result['inserted']} articles")
            )

    def run_collection_async(self, options):
        """Run data collection asynchronously using Celery"""
        try:
            from data_ingestion.tasks import collect_tweets_task, collect_news_task
            
            query = options['query']
            
            # Start async tasks
            tweet_task = collect_tweets_task.delay(query, options['tweets'])
            news_task = collect_news_task.delay(query, options['news'])
            
            self.stdout.write('⏳ Waiting for collection tasks to complete...')
            
            # Wait for completion
            tweet_result = tweet_task.get(timeout=300)  # 5 minute timeout
            news_result = news_task.get(timeout=300)
            
            self.stdout.write(
                self.style.SUCCESS(f"✅ Async collection completed")
            )
            
        except ImportError:
            self.stdout.write(
                self.style.ERROR("❌ Celery not available, falling back to sync")
            )
            self.run_collection_sync(options)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Async collection failed: {e}")
            )

    def run_processing_sync(self):
        """Run text processing synchronously"""
        cleaning_service = TextCleaningService()
        
        # Process tweets
        tweets_processed = cleaning_service.process_tweets()
        self.stdout.write(
            self.style.SUCCESS(f"✅ Processed {tweets_processed} tweets")
        )
        
        # Process articles
        articles_processed = cleaning_service.process_articles()
        self.stdout.write(
            self.style.SUCCESS(f"✅ Processed {articles_processed} articles")
        )

    def run_processing_async(self):
        """Run text processing asynchronously using Celery"""
        try:
            from text_processing.tasks import process_tweets_task, process_articles_task
            
            # Start async tasks
            tweet_task = process_tweets_task.delay()
            article_task = process_articles_task.delay()
            
            self.stdout.write('⏳ Waiting for processing tasks to complete...')
            
            # Wait for completion
            tweet_result = tweet_task.get(timeout=600)  # 10 minute timeout
            article_result = article_task.get(timeout=600)
            
            self.stdout.write(
                self.style.SUCCESS("✅ Async processing completed")
            )
            
        except ImportError:
            self.stdout.write(
                self.style.ERROR("❌ Celery not available, falling back to sync")
            )
            self.run_processing_sync()
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Async processing failed: {e}")
            )

    def print_summary(self):
        """Print pipeline summary"""
        total_tweets = Tweet.objects.count()
        total_articles = NewsArticle.objects.count()
        processed_tweets = Tweet.objects.exclude(cleaned_text__isnull=True).count()
        processed_articles = NewsArticle.objects.exclude(cleaned_text__isnull=True).count()
        
        self.stdout.write(
            self.style.SUCCESS('\n📈 Pipeline Summary:')
        )
        self.stdout.write(f"   Total tweets: {total_tweets}")
        self.stdout.write(f"   Processed tweets: {processed_tweets}")
        self.stdout.write(f"   Total articles: {total_articles}")
        self.stdout.write(f"   Processed articles: {processed_articles}")
        
        if total_tweets > 0:
            tweet_percentage = (processed_tweets / total_tweets) * 100
            self.stdout.write(f"   Tweet processing: {tweet_percentage:.1f}% complete")
        
        if total_articles > 0:
            article_percentage = (processed_articles / total_articles) * 100
            self.stdout.write(f"   Article processing: {article_percentage:.1f}% complete")