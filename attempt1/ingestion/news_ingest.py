from newsapi import NewsApiClient
import yaml
import os
import sys

# Add parent directory to path to import storage.db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage.db import db, config, db_connected

def collect_news(query="misinformation OR fake news", page_size=5):
    """
    Collect news articles matching query and insert into MongoDB.
    """
    if not config:
        print("❌ Configuration not loaded")
        return
    
    if not db_connected:
        print("❌ Database not connected")
        return
    
    try:
        api_key = config["newsapi"]["api_key"]
        if api_key == "your_newsapi_key_here":
            print("❌ Please set your NewsAPI key in config.yaml")
            return
            
        newsapi = NewsApiClient(api_key=api_key)
        print(f"📰 Fetching news for query: {query}")

        articles = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="publishedAt",
            page_size=page_size
        )

        if not articles.get("articles"):
            print("⚠️ No news articles found.")
            return

        inserted_count = 0
        for article in articles["articles"]:
            # Skip if article already exists
            existing = db.news.find_one({"url": article.get("url")})
            if existing:
                continue
                
            doc = {
                "platform": "newsapi",
                "source": article.get("source", {}).get("name", "Unknown") if article.get("source") else "Unknown",
                "author": article.get("author"),
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "publishedAt": article.get("publishedAt"),
                "content": article.get("content")
            }
            db.news.insert_one(doc)
            inserted_count += 1

        print(f"✅ Inserted {inserted_count} new news articles into MongoDB")
        
    except Exception as e:
        print(f"❌ Error collecting news: {e}")