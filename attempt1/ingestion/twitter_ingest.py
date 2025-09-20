import tweepy
import yaml
import os
import sys

# Add parent directory to path to import storage.db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage.db import db, config, db_connected

def collect_tweets(query="misinformation OR fake news", max_results=10):
    """
    Collect recent tweets matching query and insert into MongoDB.
    """
    if not config:
        print("❌ Configuration not loaded")
        return
    
    if not db_connected:
        print("❌ Database not connected")
        return
    
    try:
        bearer_token = config["twitter"]["bearer_token"]
        if bearer_token == "your_twitter_bearer_token_here":
            print("❌ Please set your Twitter Bearer Token in config.yaml")
            return
            
        client_twitter = tweepy.Client(bearer_token=bearer_token)
        print(f"🔍 Fetching tweets for query: {query}")

        tweets = client_twitter.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["created_at", "text", "author_id", "lang"]
        )

        if not tweets or not tweets.data:
            print("⚠️ No tweets found.")
            return

        inserted_count = 0
        for tweet in tweets.data:
            # Skip if tweet already exists
            existing = db.tweets.find_one({"tweet_id": str(tweet.id)})
            if existing:
                continue
                
            doc = {
                "platform": "twitter",
                "tweet_id": str(tweet.id),
                "author_id": str(tweet.author_id) if tweet.author_id else None,
                "created_at": tweet.created_at,
                "lang": tweet.lang,
                "text": tweet.text
            }
            db.tweets.insert_one(doc)
            inserted_count += 1

        print(f"✅ Inserted {inserted_count} new tweets into MongoDB")
        
    except Exception as e:
        print(f"❌ Error collecting tweets: {e}")