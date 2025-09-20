#!/usr/bin/env python3
"""
Main script to run the Twitter fact-checking bot
"""
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.twitter_bot import TwitterFactCheckBot

def main():
    print("=" * 50)
    print("🚀 Starting Twitter Fact-Checking Bot...")
    print("Press Ctrl+C to stop the bot")
    print("=" * 50)
    
    try:
        bot = TwitterFactCheckBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n✅ Bot stopped gracefully")
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")
        print("\n💡 Make sure you have:")
        print("1. Updated config/config.yaml with your Twitter API credentials")
        print("2. Set the correct bot username in config")
        print("3. Installed required packages: pip install tweepy pyyaml")

if __name__ == "__main__":
    main()