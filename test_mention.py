"""
Script to test the bot by mentioning it in a test tweet
This helps you see if the bot is working correctly
"""
import tweepy
import yaml

def load_config():
    with open("config/config.yaml", 'r') as f:
        return yaml.safe_load(f)

def test_bot():
    config = load_config()
    
    # Setup Twitter API
    client = tweepy.Client(
        bearer_token=config['twitter']['bearer_token'],
        consumer_key=config['twitter']['api_key'],
        consumer_secret=config['twitter']['api_secret'],
        access_token=config['twitter']['access_token'],
        access_token_secret=config['twitter']['access_token_secret'],
        wait_on_rate_limit=True
    )
    
    bot_username = config['bot']['username']
    
    # Test tweets to try
    test_tweets = [
        f"Testing my fact-checking bot! @{bot_username} This is a test message with no claims.",
        f"@{bot_username} Breaking news: Scientists have discovered a miracle cure that doctors don't want you to know about!",
        f"Hey @{bot_username} can you check this: According to BBC, the weather was nice today."
    ]
    
    print(f"🧪 Testing bot @{bot_username}")
    print("\nChoose a test tweet to post:")
    
    for i, tweet in enumerate(test_tweets, 1):
        print(f"{i}. {tweet}")
    
    choice = input("\nEnter choice (1-3) or 'q' to quit: ").strip()
    
    if choice == 'q':
        return
    
    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(test_tweets):
            tweet_text = test_tweets[choice_idx]
            
            # Post the test tweet
            response = client.create_tweet(text=tweet_text)
            print(f"✅ Test tweet posted: {tweet_text}")
            print(f"🔗 Tweet ID: {response.data['id']}")
            print(f"\n⏰ Wait a moment for your bot to respond...")
            
        else:
            print("❌ Invalid choice")
            
    except Exception as e:
        print(f"❌ Error posting test tweet: {e}")

if __name__ == "__main__":
    test_bot()