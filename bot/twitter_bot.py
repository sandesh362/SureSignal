# bot/twitter_bot.py (Updated with Windows-compatible logging)
import tweepy
import yaml
import time
import logging
from typing import Optional, List, Dict
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.fact_checker import FactChecker

# Set up Windows-compatible logging (no emojis in logs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TwitterFactCheckBot:
    """
    Twitter bot that responds to mentions with fact-checking analysis
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = self._load_config(config_path)
        self.api = self._setup_twitter_api()
        self.fact_checker = FactChecker()
        self.processed_tweets = set()
        self.bot_username = self.config['bot']['username']
        
        logger.info(f"Bot initialized as @{self.bot_username}")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise
    
    def _setup_twitter_api(self) -> tweepy.API:
        """Setup Twitter API connection with both v1.1 and v2"""
        try:
            # V1.1 API (for posting replies)
            auth = tweepy.OAuthHandler(
                self.config['twitter']['api_key'],
                self.config['twitter']['api_secret']
            )
            auth.set_access_token(
                self.config['twitter']['access_token'],
                self.config['twitter']['access_token_secret']
            )
            api_v1 = tweepy.API(auth, wait_on_rate_limit=True)
            
            # V2 API (for searching mentions)
            self.client_v2 = tweepy.Client(
                bearer_token=self.config['twitter']['bearer_token'],
                consumer_key=self.config['twitter']['api_key'],
                consumer_secret=self.config['twitter']['api_secret'],
                access_token=self.config['twitter']['access_token'],
                access_token_secret=self.config['twitter']['access_token_secret'],
                wait_on_rate_limit=True
            )
            
            # Test the connection
            api_v1.verify_credentials()
            logger.info("Twitter API connection successful")
            
            return api_v1
            
        except Exception as e:
            logger.error(f"Failed to setup Twitter API: {e}")
            raise
    
    def get_mentions(self) -> List[tweepy.models.Status]:
        """Get recent mentions of the bot"""
        try:
            # Use v2 API to search for mentions
            query = f"@{self.bot_username} -is:retweet"
            tweets = self.client_v2.search_recent_tweets(
                query=query,
                max_results=10,
                tweet_fields=['created_at', 'author_id', 'context_annotations', 'conversation_id'],
                expansions=['author_id', 'in_reply_to_user_id'],
                user_fields=['username']
            )
            
            if not tweets.data:
                return []
            
            mentions = []
            users_dict = {user.id: user for user in tweets.includes.get('users', [])}
            
            for tweet in tweets.data:
                # Skip if already processed
                if str(tweet.id) in self.processed_tweets:
                    continue
                
                author = users_dict.get(tweet.author_id)
                if author:
                    mentions.append({
                        'id': str(tweet.id),
                        'text': tweet.text,
                        'author_username': author.username,
                        'conversation_id': tweet.conversation_id,
                        'created_at': tweet.created_at
                    })
            
            return mentions
            
        except Exception as e:
            logger.error(f"Error getting mentions: {e}")
            return []
    
    def get_tweet_to_check(self, mention: Dict) -> Optional[str]:
        """
        Get the tweet that should be fact-checked.
        If the mention is a reply, get the original tweet.
        Otherwise, check the mention itself.
        """
        try:
            # If this is part of a conversation, get the original tweet
            if mention['conversation_id'] != mention['id']:
                original_tweet = self.client_v2.get_tweet(
                    mention['conversation_id'],
                    tweet_fields=['text', 'author_id'],
                    expansions=['author_id'],
                    user_fields=['username']
                )
                
                if original_tweet.data:
                    return original_tweet.data.text
            
            # Otherwise, check the mention itself (remove the bot mention)
            tweet_text = mention['text']
            # Remove the bot mention from the text
            tweet_text = tweet_text.replace(f"@{self.bot_username}", "").strip()
            
            return tweet_text if tweet_text else None
            
        except Exception as e:
            logger.error(f"Error getting tweet to check: {e}")
            return mention['text']
    
    def process_mention(self, mention: Dict) -> bool:
        """Process a single mention"""
        try:
            logger.info(f"Processing mention from @{mention['author_username']}: {mention['text'][:100]}...")
            
            # Get the text to fact-check
            text_to_check = self.get_tweet_to_check(mention)
            if not text_to_check or len(text_to_check) < 10:
                logger.info("No substantial content to fact-check, skipping")
                return False
            
            # Perform fact-checking
            analysis = self.fact_checker.analyze_tweet(text_to_check)
            logger.info(f"Analysis result: {analysis['status']} (confidence: {analysis['confidence']:.2f})")
            
            # Generate response
            response = self.fact_checker.generate_response(analysis, mention['author_username'])
            
            # Post reply
            self.api.update_status(
                status=response,
                in_reply_to_status_id=int(mention['id']),
                auto_populate_reply_metadata=True
            )
            
            logger.info(f"Posted reply: {response}")
            print(f"[REPLY SENT] {response}")  # Console output without logging issues
            
            # Mark as processed
            self.processed_tweets.add(mention['id'])
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing mention {mention['id']}: {e}")
            return False
    
    def run(self):
        """Main bot loop"""
        print("🤖 Fact-checking bot started!")
        print(f"📱 Monitoring mentions of @{self.bot_username}")
        print("⏹️  Press Ctrl+C to stop")
        print("-" * 50)
        
        logger.info("Fact-checking bot started")
        logger.info(f"Monitoring mentions of @{self.bot_username}")
        
        check_interval = self.config['bot']['check_interval']
        
        try:
            while True:
                logger.info("Checking for new mentions...")
                
                mentions = self.get_mentions()
                if mentions:
                    print(f"📬 Found {len(mentions)} new mention(s)")
                    logger.info(f"Found {len(mentions)} new mention(s)")
                    
                    for mention in mentions:
                        try:
                            self.process_mention(mention)
                            time.sleep(2)  # Rate limiting between responses
                        except Exception as e:
                            logger.error(f"Failed to process mention: {e}")
                            continue
                else:
                    logger.info("No new mentions found")
                
                print(f"⏰ Waiting {check_interval} seconds before next check...")
                logger.info(f"Waiting {check_interval} seconds before next check")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n✅ Bot stopped by user")
            logger.info("Bot stopped by user")
        except Exception as e:
            print(f"❌ Bot error: {e}")
            logger.error(f"Bot error: {e}")
            raise