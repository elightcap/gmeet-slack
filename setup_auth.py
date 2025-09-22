#!/usr/bin/env python3
"""
Google OAuth Setup Script for Docker Environment

This script helps set up Google OAuth authentication in a headless environment.
Run this script once to generate the token.json file, then copy it to your container.
"""

import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from config import Config

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def setup_google_auth():
    """Set up Google OAuth authentication"""
    print("🔐 Setting up Google OAuth authentication...")
    
    # Check if credentials file exists
    if not os.path.exists(Config.GOOGLE_CREDENTIALS_FILE):
        print(f"❌ Google credentials file not found: {Config.GOOGLE_CREDENTIALS_FILE}")
        print("Please download your OAuth2 credentials from Google Cloud Console and save as 'credentials.json'")
        return False
    
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists(Config.GOOGLE_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(Config.GOOGLE_TOKEN_FILE, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("🌐 Starting OAuth flow...")
            print("This will open a browser window for authentication.")
            print("If you're running in a headless environment, you'll need to:")
            print("1. Copy the authorization URL from the output")
            print("2. Open it in a browser on your local machine")
            print("3. Complete the authentication")
            print("4. Copy the authorization code back to this script")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                Config.GOOGLE_CREDENTIALS_FILE, SCOPES)
            
            try:
                # Try to run with browser first
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"⚠️  Browser authentication failed: {e}")
                print("🔄 Trying headless authentication...")
                
                # Fallback to headless authentication
                creds = flow.run_local_server(port=0, open_browser=False)
        
        # Save the credentials for the next run
        print("💾 Saving credentials...")
        with open(Config.GOOGLE_TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    print("✅ Google OAuth authentication setup complete!")
    print(f"📁 Token saved to: {Config.GOOGLE_TOKEN_FILE}")
    return True

if __name__ == "__main__":
    success = setup_google_auth()
    sys.exit(0 if success else 1)
