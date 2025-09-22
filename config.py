import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Slack Configuration
    SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
    SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
    SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')
    
    # Google Calendar Configuration
    GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
    GOOGLE_TOKEN_FILE = os.getenv('GOOGLE_TOKEN_FILE', 'token.json')
    
    # Bot Configuration
    BOT_USER_ID = os.getenv('BOT_USER_ID')
    
    # Meeting Configuration
    MEETING_DURATION_MINUTES = 60  # Default meeting duration
    CALENDAR_ID = 'primary'  # Use primary calendar
