from django.core.management.base import BaseCommand
from text_processing.services import TextCleaningService
from core.models import Tweet, NewsArticle

class Command(BaseCommand):
    help = 'Process text data for tweets and news articles'

    def add_arguments(self, parser):
        parser.add_argument('--tweets-limit', type=int, default=None,
                          help='Limit number of tweets to process')
        parser.add_argument('--articles-limit', type=int, default=None,
                          help='Limit number of articles to process')
        parser.add_argument('--skip-tweets', action='store_true',
                          help='Skip tweet text processing')
        parser.add_argument('--skip-articles', action='store_true',
                          help='Skip article text processing')

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting text processing pipeline...')
        )

        cleaning_service = TextCleaningService()

        if not options['skip_tweets']:
            self.stdout.write('🔄 Processing tweets...')
            tweets_processed = cleaning_service.process_tweets(
                limit=options['tweets_limit']
            )
            self.stdout.write(
                self.style.SUCCESS(f"✅ Processed {tweets_processed} tweets")
            )

        if not options['skip_articles']:
            self.stdout.write('🔄 Processing articles...')
            articles_processed = cleaning_service.process_articles(
                limit=options['articles_limit']
            )
            self.stdout.write(
                self.style.SUCCESS(f"✅ Processed {articles_processed} articles")
            )

        # Print summary
        total_tweets = Tweet.objects.count()
        total_articles = NewsArticle.objects.count()
        processed_tweets = Tweet.objects.exclude(cleaned_text__isnull=True).count()
        processed_articles = NewsArticle.objects.exclude(cleaned_text__isnull=True).count()
        
        self.stdout.write(
            self.style.SUCCESS('\n📈 Processing Summary:')
        )
        self.stdout.write(f"   Total tweets: {total_tweets}")
        self.stdout.write(f"   Processed tweets: {processed_tweets}")
        self.stdout.write(f"   Total articles: {total_articles}")
        self.stdout.write(f"   Processed articles: {processed_articles}")
        
        self.stdout.write(
            self.style.SUCCESS('✅ Text processing completed!')
        )