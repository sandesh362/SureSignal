from django.core.management.base import BaseCommand
from data_ingestion.services import TwitterService, NewsService

class Command(BaseCommand):
    help = 'Collect data from Twitter and News APIs'

    def add_arguments(self, parser):
        parser.add_argument('--query', type=str, default='misinformation OR fake news',
                          help='Search query')
        parser.add_argument('--tweets', type=int, default=10,
                          help='Number of tweets to collect')
        parser.add_argument('--news', type=int, default=5,
                          help='Number of news articles to collect')
        parser.add_argument('--skip-twitter', action='store_true',
                          help='Skip Twitter data collection')
        parser.add_argument('--skip-news', action='store_true',
                          help='Skip news data collection')

    def handle(self, *args, **options):
        query = options['query']
        
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting data collection pipeline...')
        )

        if not options['skip_twitter']:
            self.stdout.write('📊 Collecting tweets...')
            twitter_service = TwitterService()
            tweets_result = twitter_service.collect_tweets(
                query=query, 
                max_results=options['tweets']
            )
            
            if 'error' in tweets_result:
                self.stdout.write(
                    self.style.ERROR(f"❌ Twitter collection failed: {tweets_result['error']}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Collected {tweets_result['inserted']} tweets")
                )

        if not options['skip_news']:
            self.stdout.write('📰 Collecting news articles...')
            news_service = NewsService()
            news_result = news_service.collect_news(
                query=query, 
                page_size=options['news']
            )
            
            if 'error' in news_result:
                self.stdout.write(
                    self.style.ERROR(f"❌ News collection failed: {news_result['error']}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Collected {news_result['inserted']} articles")
                )

        self.stdout.write(
            self.style.SUCCESS('✅ Data collection completed!')
        )