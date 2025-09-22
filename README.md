# Google Meet Slack Bot

A Slack bot that allows users to create Google Meet meetings using the `/meet` slash command. Users can create meetings with custom titles and durations directly from Slack.

## Features

- 🎯 **Simple Command**: Use `/meet` to create instant Google Meet meetings
- ⏰ **Custom Duration**: Specify meeting duration (e.g., `/meet Team Standup 30m`)
- 📝 **Custom Titles**: Add custom meeting titles (e.g., `/meet Weekly Sync`)
- 🔗 **Direct Links**: Get Google Meet links and calendar event links
- 💬 **Channel Support**: Works in channels and direct messages
- 🎨 **Rich UI**: Beautiful Slack blocks with action buttons

## Prerequisites

- Python 3.7+
- Slack App with appropriate permissions
- Google Cloud Project with Calendar API enabled
- Google OAuth2 credentials

## Installation

1. **Clone or download this project**
   ```bash
   cd git/gmeetslack
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

4. **Set up Google Calendar API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the Google Calendar API
   - Create OAuth2 credentials (Desktop application)
   - Download the credentials file as `credentials.json`

5. **Set up Slack App**
   - Go to [api.slack.com](https://api.slack.com/apps)
   - Create a new app
   - Configure OAuth & Permissions
   - Add the following scopes:
     - `chat:write`
     - `commands`
     - `app_mentions:read`
     - `im:read`
     - `im:write`
   - Create a slash command `/meet`
   - Install the app to your workspace

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Slack Bot Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
SLACK_APP_TOKEN=xapp-your-app-token-here

# Google Calendar API Configuration
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.json

# Bot Configuration
BOT_USER_ID=U1234567890
```

### Google Calendar Setup

1. Place your `credentials.json` file in the project root
2. Run the bot once to authenticate with Google (it will open a browser)
3. The `token.json` file will be created automatically

## Usage

### Basic Usage

```
/meet
```
Creates a 60-minute meeting titled "Quick Meeting"

### Advanced Usage

```
/meet Team Standup 30m
```
Creates a 30-minute meeting titled "Team Standup"

```
/meet Weekly Sync 2h
```
Creates a 2-hour meeting titled "Weekly Sync"

### Duration Formats

- `30m` - 30 minutes
- `1h` - 1 hour
- `2h30m` - 2 hours 30 minutes
- `90m` - 90 minutes

## Running the Bot

```bash
python main.py
```

The bot will:
1. Check for required environment variables
2. Verify Google credentials
3. Start the Slack bot
4. Listen for `/meet` commands

## Bot Responses

When you use `/meet`, the bot will respond with:

- ✅ Meeting title and duration
- 🔗 Direct Google Meet link
- 📋 Calendar event link
- 🎯 Action buttons to join or view in calendar

## Troubleshooting

### Common Issues

1. **"Missing required environment variables"**
   - Check your `.env` file
   - Ensure all required variables are set

2. **"Google credentials file not found"**
   - Download `credentials.json` from Google Cloud Console
   - Place it in the project root directory

3. **"Authentication failed"**
   - Delete `token.json` and run the bot again
   - Complete the OAuth flow in your browser

4. **"Slack API error"**
   - Verify your Slack app tokens
   - Check that the bot has necessary permissions
   - Ensure the slash command is properly configured

### Logs

The bot will display helpful error messages in the console. Check these for debugging information.

## Development

### Project Structure

```
git/gmeetslack/
├── main.py                 # Main application entry point
├── config.py              # Configuration management
├── slack_handlers.py      # Slack bot event handlers
├── google_calendar.py     # Google Calendar API integration
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
├── README.md             # This file
└── credentials.json      # Google OAuth2 credentials (you add this)
```

### Adding Features

1. **New slash commands**: Add handlers in `slack_handlers.py`
2. **Calendar features**: Extend `google_calendar.py`
3. **Configuration**: Update `config.py`

## Security Notes

- Never commit `credentials.json` or `.env` files
- Use environment variables for sensitive data
- Regularly rotate your Slack tokens
- Monitor bot usage and permissions

## License

This project is open source. Feel free to modify and distribute as needed.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Slack and Google API documentation
3. Check the console logs for error messages
