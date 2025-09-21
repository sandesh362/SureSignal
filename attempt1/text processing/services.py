import re
import nltk
from nltk.corpus import stopwords
from core.models import Tweet, NewsArticle
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

# Download stopwords with error handling
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    logger.info("📦 Downloading NLTK stopwords...")
    nltk.download("stopwords", quiet=True)

try:
    STOPWORDS = set(stopwords.words("english"))
except Exception as e:
    logger.warning(f"⚠️ Could not load stopwords: {e}")
    STOPWORDS = set()

# Try to load spaCy model with fallback
try:
    import spacy
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
    SPACY_AVAILABLE = True
    logger.info("✅ spaCy model loaded successfully")
except (ImportError, OSError) as e:
    logger.warning(f"⚠️ spaCy not available: {e}")
    logger.info("💡 Install with: python -m spacy download en_core_web_sm")
    SPACY_AVAILABLE = False

class TextCleaningService:
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text for NLP processing.
        Steps:
          - Lowercasing
          - Remove URLs, mentions, hashtags, numbers
          - Remove punctuation/special chars
          - Remove stopwords
          - Lemmatization (if spaCy available)
        """
        if not isinstance(text, str) or not text.strip():
            return ""

        # Lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r"http\S+|www\S+|https\S+", "", text)

        # Remove mentions, hashtags
        text = re.sub(r"@\w+|#\w+", "", text)

        # Remove numbers
        text = re.sub(r"\d+", "", text)

        # Remove emojis/special chars
        text = re.sub(r"[^a-zA-Z\s]", "", text)

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)

        if SPACY_AVAILABLE:
            # Lemmatization + stopword removal with spaCy
            doc = nlp(text)
            cleaned = " ".join([
                token.lemma_ for token in doc 
                if token.lemma_ not in STOPWORDS and len(token.lemma_) > 2
            ])
        else:
            # Basic stopword removal without lemmatization
            words = text.split()
            cleaned = " ".join([
                word for word in words 
                if word not in STOPWORDS and len(word) > 2
            ])

        return cleaned.strip()

    def process_tweets(self, limit=None):
        """Process unprocessed tweets"""
        tweets_queryset = Tweet.objects.filter(cleaned_text__isnull=True)
        if limit:
            tweets_queryset = tweets_queryset[:limit]
        
        processed_count = 0
        for tweet in tweets_queryset:
            if tweet.text:
                cleaned = self.clean_text(tweet.text)
                if cleaned:  # Only update if cleaning produced results
                    tweet.cleaned_text = cleaned
                    tweet.save(update_fields=['cleaned_text'])
                    processed_count += 1
        
        logger.info(f"✅ Processed {processed_count} tweets")
        return processed_count

    def process_articles(self, limit=None):
        """Process unprocessed news articles"""
        articles_queryset = NewsArticle.objects.filter(cleaned_text__isnull=True)
        if limit:
            articles_queryset = articles_queryset[:limit]
        
        processed_count = 0
        for article in articles_queryset:
            title = article.title or ""
            description = article.description or ""
            combined = f"{title} {description}".strip()
            
            if combined:
                cleaned = self.clean_text(combined)
                if cleaned:  # Only update if cleaning produced results
                    article.cleaned_text = cleaned
                    article.save(update_fields=['cleaned_text'])
                    processed_count += 1
        
        logger.info(f"✅ Processed {processed_count} articles")
        return processed_count

    def process_all(self, tweet_limit=None, article_limit=None):
        """Process both tweets and articles"""
        tweets_processed = self.process_tweets(limit=tweet_limit)
        articles_processed = self.process_articles(limit=article_limit)
        
        return {
            'tweets_processed': tweets_processed,
            'articles_processed': articles_processed,
            'total_processed': tweets_processed + articles_processed
        }



