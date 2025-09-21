import tweepy
from newsapi import NewsApiClient
from django.conf import settings
from core.models import Tweet, NewsArticle
from django.utils import timezone
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TwitterService:
    def __init__(self):
        self.bearer_token = getattr(settings, 'TWITTER_CONFIG', {}).get('bearer_token')
        if not self.bearer_token or self.bearer_token == "your_twitter_bearer_token_here":
            logger.error("Twitter Bearer Token not configured")
            self.client = None
        else:
            self.client = tweepy.Client(bearer_token=self.bearer_token)
    
    def collect_tweets(self, query="misinformation OR fake news", max_results=10):
        """Collect recent tweets matching query and save to database."""
        if not self.client:
            logger.error("Twitter client not initialized")
            return {'error': 'Twitter client not configured', 'inserted': 0}
        
        try:
            logger.info(f"🔍 Fetching tweets for query: {query}")
            
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=["created_at", "text", "author_id", "lang"]
            )
            
            if not tweets or not tweets.data:
                logger.warning("⚠️ No tweets found.")
                return {'error': 'No tweets found', 'inserted': 0}
            
            inserted_count = 0
            for tweet in tweets.data:
                # Check if tweet already exists
                if Tweet.objects.filter(tweet_id=str(tweet.id)).exists():
                    continue
                
                # Create new tweet object
                tweet_obj = Tweet(
                    platform="twitter",
                    tweet_id=str(tweet.id),
                    author_id=str(tweet.author_id) if tweet.author_id else None,
                    created_at=tweet.created_at or timezone.now(),
                    lang=tweet.lang,
                    text=tweet.text
                )
                tweet_obj.save()
                inserted_count += 1
            
            logger.info(f"✅ Inserted {inserted_count} new tweets")
            return {'success': True, 'inserted': inserted_count}
            
        except Exception as e:
            logger.error(f"❌ Error collecting tweets: {e}")
            return {'error': str(e), 'inserted': 0}

class NewsService:
    def __init__(self):
        self.api_key = getattr(settings, 'NEWSAPI_CONFIG', {}).get('api_key')
        if not self.api_key or self.api_key == "your_newsapi_key_here":
            logger.error("NewsAPI key not configured")
            self.client = None
        else:
            self.client = NewsApiClient(api_key=self.api_key)
    
    def collect_news(self, query="misinformation OR fake news", page_size=5):
        """Collect news articles matching query and save to database."""
        if not self.client:
            logger.error("NewsAPI client not initialized")
            return {'error': 'NewsAPI client not configured', 'inserted': 0}
        
        try:
            logger.info(f"📰 Fetching news for query: {query}")
            
            articles = self.client.get_everything(
                q=query,
                language="en",
                sort_by="publishedAt",
                page_size=page_size
            )
            
            if not articles.get("articles"):
                logger.warning("⚠️ No news articles found.")
                return {'error': 'No articles found', 'inserted': 0}
            
            inserted_count = 0
            for article in articles["articles"]:
                # Check if article already exists
                if NewsArticle.objects.filter(url=article.get("url")).exists():
                    continue
                
                # Parse published date
                published_at = article.get("publishedAt")
                if published_at:
                    published_at = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                else:
                    published_at = timezone.now()
                
                # Create new article object
                article_obj = NewsArticle(
                    platform="newsapi",
                    source=article.get("source", {}).get("name", "Unknown") if article.get("source") else "Unknown",
                    author=article.get("author"),
                    title=article.get("title"),
                    description=article.get("description"),
                    url=article.get("url"),
                    published_at=published_at,
                    content=article.get("content")
                )
                article_obj.save()
                inserted_count += 1
            
            logger.info(f"✅ Inserted {inserted_count} new news articles")
            return {'success': True, 'inserted': inserted_count}
            
        except Exception as e:
            logger.error(f"❌ Error collecting news: {e}")
            return {'error': str(e), 'inserted': 0}
