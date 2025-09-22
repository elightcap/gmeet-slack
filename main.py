#!/usr/bin/env python3
"""
Google Meet Slack Bot

A Slack bot that allows users to create Google Meet meetings using the /meet command.
"""

import os
import sys
from slack_handlers import SlackBotHandlers
from config import Config

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        'SLACK_BOT_TOKEN',
        'SLACK_SIGNING_SECRET', 
        'SLACK_APP_TOKEN'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not getattr(Config, var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        print("See env.example for reference.")
        return False
    
    return True

def check_google_credentials():
    """Check if Google credentials file exists"""
    if not os.path.exists(Config.GOOGLE_CREDENTIALS_FILE):
        print(f"❌ Google credentials file not found: {Config.GOOGLE_CREDENTIALS_FILE}")
        print("Please download your OAuth2 credentials from Google Cloud Console and save as 'credentials.json'")
        return False
    
    # Check if token file exists
    if not os.path.exists(Config.GOOGLE_TOKEN_FILE):
        print(f"⚠️  Google token file not found: {Config.GOOGLE_TOKEN_FILE}")
        print("You need to run the authentication setup first:")
        print("1. Run: python setup_auth.py")
        print("2. Complete the OAuth flow")
        print("3. Then restart the bot")
        return False
    
    return True

def main():
    """Main application entry point"""
    print("🚀 Starting Google Meet Slack Bot...")
    
    # Check environment variables
    if not check_environment():
        sys.exit(1)
    
    # Check Google credentials
    if not check_google_credentials():
        sys.exit(1)
    
    try:
        # Initialize and start the bot
        bot = SlackBotHandlers()
        print("✅ Bot initialized successfully!")
        print("📱 Bot is now running. Press Ctrl+C to stop.")
        bot.start()
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
