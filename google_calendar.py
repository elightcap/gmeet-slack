import os
import pickle
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import Config

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarService:
    def __init__(self):
        self.service = None
        self.credentials = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists(Config.GOOGLE_TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(Config.GOOGLE_TOKEN_FILE, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(Config.GOOGLE_CREDENTIALS_FILE):
                    raise FileNotFoundError(
                        f"Google credentials file not found: {Config.GOOGLE_CREDENTIALS_FILE}\n"
                        "Please download your OAuth2 credentials from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    Config.GOOGLE_CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(Config.GOOGLE_TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        self.credentials = creds
        self.service = build('calendar', 'v3', credentials=creds)
    
    def create_meeting(self, title="Quick Meeting", duration_minutes=60, description=""):
        """
        Create a Google Meet meeting and return the meeting details
        
        Args:
            title (str): Meeting title
            duration_minutes (int): Meeting duration in minutes
            description (str): Meeting description
            
        Returns:
            dict: Meeting details including Meet link
        """
        try:
            # Calculate start and end times
            now = datetime.utcnow()
            start_time = now.isoformat() + 'Z'
            end_time = (now + timedelta(minutes=duration_minutes)).isoformat() + 'Z'
            
            # Create the event
            event = {
                'summary': title,
                'description': description,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'UTC',
                },
                'conferenceData': {
                    'createRequest': {
                        'requestId': f"meet-{now.strftime('%Y%m%d%H%M%S')}",
                        'conferenceSolutionKey': {
                            'type': 'hangoutsMeet'
                        }
                    }
                },
                'attendees': [],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 10},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            
            # Create the event with conference data
            event = self.service.events().insert(
                calendarId=Config.CALENDAR_ID,
                body=event,
                conferenceDataVersion=1
            ).execute()
            
            # Extract meeting details
            meet_link = event.get('conferenceData', {}).get('entryPoints', [{}])[0].get('uri', '')
            meeting_id = event.get('id', '')
            
            return {
                'success': True,
                'meeting_id': meeting_id,
                'meet_link': meet_link,
                'title': event.get('summary', title),
                'start_time': event.get('start', {}).get('dateTime', start_time),
                'end_time': event.get('end', {}).get('dateTime', end_time),
                'calendar_link': event.get('htmlLink', ''),
                'event_id': event.get('id', '')
            }
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return {
                'success': False,
                'error': str(error)
            }
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            return {
                'success': False,
                'error': str(error)
            }
    
    def get_meeting_info(self, meeting_id):
        """Get information about a specific meeting"""
        try:
            event = self.service.events().get(
                calendarId=Config.CALENDAR_ID,
                eventId=meeting_id
            ).execute()
            
            meet_link = event.get('conferenceData', {}).get('entryPoints', [{}])[0].get('uri', '')
            
            return {
                'success': True,
                'meeting_id': event.get('id', ''),
                'meet_link': meet_link,
                'title': event.get('summary', ''),
                'start_time': event.get('start', {}).get('dateTime', ''),
                'end_time': event.get('end', {}).get('dateTime', ''),
                'calendar_link': event.get('htmlLink', ''),
                'description': event.get('description', '')
            }
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return {
                'success': False,
                'error': str(error)
            }
