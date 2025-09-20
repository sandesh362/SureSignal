import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion import twitter_ingest, news_ingest

def test_twitter_collect():
    """Test that twitter_ingest has collect_tweets function"""
    assert hasattr(twitter_ingest, "collect_tweets")
    print("✅ Twitter collect_tweets function exists")

def test_news_collect():
    """Test that news_ingest has collect_news function"""
    assert hasattr(news_ingest, "collect_news")
    print("✅ News collect_news function exists")

if __name__ == "__main__":
    test_twitter_collect()
    test_news_collect()
    print("✅ All tests passed!")