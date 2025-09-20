import sys
import os

# Ensure all modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🚀 Misinformation Detection Pipeline Starting...")
    
    try:
        # Import modules with error handling
        from storage.db import db, db_connected
        from preprocessing.clean_text import clean_text
        from ingestion import twitter_ingest, news_ingest
        
        if not db_connected:
            print("❌ Database connection failed. Exiting.")
            return
        
        # Run ingestion
        print("\n📊 Starting data collection...")
        twitter_ingest.collect_tweets(query="fake news OR misinformation", max_results=10)
        news_ingest.collect_news(query="fake news OR misinformation", page_size=5)

        print("\n🔄 Starting text preprocessing...")
        
        # Apply preprocessing on tweets
        tweets_processed = 0
        tweets = db.tweets.find({"cleaned_text": {"$exists": False}})
        for tweet in tweets:
            if tweet.get("text"):
                cleaned = clean_text(tweet["text"])
                if cleaned:  # Only update if cleaning produced results
                    db.tweets.update_one(
                        {"_id": tweet["_id"]}, 
                        {"$set": {"cleaned_text": cleaned}}
                    )
                    tweets_processed += 1

        # Apply preprocessing on news
        articles_processed = 0
        articles = db.news.find({"cleaned_text": {"$exists": False}})
        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")
            combined = f"{title} {description}".strip()
            
            if combined:
                cleaned = clean_text(combined)
                if cleaned:  # Only update if cleaning produced results
                    db.news.update_one(
                        {"_id": article["_id"]}, 
                        {"$set": {"cleaned_text": cleaned}}
                    )
                    articles_processed += 1

        print(f"✅ Processed {tweets_processed} tweets and {articles_processed} articles")
        print("✅ Data ingestion + preprocessing complete. Check MongoDB.")
        
        # Print summary
        total_tweets = db.tweets.count_documents({})
        total_articles = db.news.count_documents({})
        print(f"\n📈 Database Summary:")
        print(f"   Total tweets: {total_tweets}")
        print(f"   Total articles: {total_articles}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all directories have __init__.py files")
    except Exception as e:
        print(f"❌ Error in main pipeline: {e}")

if __name__ == '__main__':
    main()