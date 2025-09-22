from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from google_calendar import GoogleCalendarService
from config import Config
import re

class SlackBotHandlers:
    def __init__(self):
        self.app = App(
            token=Config.SLACK_BOT_TOKEN,
            signing_secret=Config.SLACK_SIGNING_SECRET
        )
        self.calendar_service = GoogleCalendarService()
        self._register_handlers()
    
    def _register_handlers(self):
        """Register all Slack event handlers"""
        
        @self.app.command("/meet")
        def handle_meet_command(ack, respond, command):
            """Handle the /meet slash command"""
            ack()
            
            try:
                # Parse command text for optional parameters
                text = command.get('text', '').strip()
                
                # Extract title and duration from command text
                title = "Quick Meeting"
                duration = 60
                description = ""
                
                if text:
                    # Try to parse duration (e.g., "30m", "1h", "2h30m")
                    duration_match = re.search(r'(\d+)([hm])', text.lower())
                    if duration_match:
                        value = int(duration_match.group(1))
                        unit = duration_match.group(2)
                        if unit == 'h':
                            duration = value * 60
                        else:  # 'm'
                            duration = value
                        # Remove duration from text to get title
                        text = re.sub(r'\d+[hm]', '', text).strip()
                    
                    # Use remaining text as title
                    if text:
                        title = text
                
                # Create the meeting
                meeting_result = self.calendar_service.create_meeting(
                    title=title,
                    duration_minutes=duration,
                    description=description
                )
                
                if meeting_result['success']:
                    # Format the response
                    response_text = f"🎉 *Meeting Created Successfully!*\n\n"
                    response_text += f"📅 *Title:* {meeting_result['title']}\n"
                    response_text += f"⏰ *Duration:* {duration} minutes\n"
                    response_text += f"🔗 *Google Meet Link:* {meeting_result['meet_link']}\n"
                    response_text += f"📋 *Calendar Event:* {meeting_result['calendar_link']}"
                    
                    # Send response to the channel/user
                    respond({
                        "text": response_text,
                        "blocks": [
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": response_text
                                }
                            },
                            {
                                "type": "actions",
                                "elements": [
                                    {
                                        "type": "button",
                                        "text": {
                                            "type": "plain_text",
                                            "text": "Join Meeting"
                                        },
                                        "url": meeting_result['meet_link'],
                                        "style": "primary"
                                    },
                                    {
                                        "type": "button",
                                        "text": {
                                            "type": "plain_text",
                                            "text": "View in Calendar"
                                        },
                                        "url": meeting_result['calendar_link']
                                    }
                                ]
                            }
                        ]
                    })
                else:
                    respond(f"❌ Sorry, I couldn't create the meeting. Error: {meeting_result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                respond(f"❌ An error occurred while creating the meeting: {str(e)}")
        
        @self.app.event("app_mention")
        def handle_app_mention(event, say):
            """Handle when the bot is mentioned"""
            say("👋 Hi! Use `/meet` to create a Google Meet meeting. You can also specify a title and duration like `/meet Team Standup 30m`")
        
        @self.app.event("message")
        def handle_message_events(event, say):
            """Handle direct messages to the bot"""
            # Only respond to direct messages (not channel messages)
            if event.get('channel_type') == 'im':
                say("👋 Hi! Use `/meet` to create a Google Meet meeting. You can also specify a title and duration like `/meet Team Standup 30m`")
    
    def start(self):
        """Start the Slack bot"""
        handler = SocketModeHandler(self.app, Config.SLACK_APP_TOKEN)
        handler.start()
