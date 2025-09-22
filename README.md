# Google Meet Slack Bot 🐳

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A containerized Slack bot that allows users to create Google Meet meetings using the `/gmeet` slash command. Users can create meetings with custom titles and durations directly from Slack.

## Features

- 🎯 **Simple Command**: Use `/gmeet` to create instant Google Meet meetings
- ⏰ **Custom Duration**: Specify meeting duration (e.g., `/gmeet Team Standup 30m`)
- 📝 **Custom Titles**: Add custom meeting titles (e.g., `/gmeet Weekly Sync`)
- 🔗 **Direct Links**: Get Google Meet links and calendar event links
- 💬 **Channel Support**: Works in channels and direct messages
- 🎨 **Rich UI**: Beautiful Slack blocks with action buttons
- 🐳 **Containerized**: Easy deployment with Docker and Docker Compose
- 🔌 **Socket Mode**: Direct connection to Slack (no web server needed)

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Slack App with appropriate permissions
- Google Cloud Project with Calendar API enabled

### 1. Clone and Setup

```bash
git clone <your-repo>
cd gmeetslack
cp env.example .env
```

### 2. Configure Environment

Edit `.env` with your actual values:

```env
# Slack Bot Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
SLACK_APP_TOKEN=xapp-your-app-token-here

# Google Calendar API Configuration
GOOGLE_CREDENTIALS_FILE=credentials/credentials.json
GOOGLE_TOKEN_FILE=credentials/token.json

# Bot Configuration
BOT_USER_ID=U1234567890
```

### 3. Add Google Credentials

```bash
mkdir -p credentials
# Place your credentials.json file in the credentials/ directory
cp /path/to/your/credentials.json credentials/

# Set up Google OAuth authentication
python setup_auth.py
```

### 4. Run the Bot

```bash
# Build and start the bot
./scripts/build.sh
./scripts/run.sh

# Or use Docker Compose directly
docker-compose up -d
```

### 5. View Logs

```bash
docker-compose logs -f
```

## Docker Commands

### Basic Operations

```bash
# Build the image
docker build -t gmeetslack-bot .

# Run the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down

# Restart the bot
docker-compose restart
```

### Development

```bash
# Run in development mode
docker-compose up -d

# View logs
docker-compose logs -f
```

### Production

```bash
# Use production configuration
docker-compose -f docker-compose.prod.yml up -d
```

## Scripts

The project includes helpful scripts in the `scripts/` directory:

- `build.sh` - Build the Docker image
- `run.sh` - Start the bot
- `stop.sh` - Stop the bot

## Usage

### Basic Usage

```
/gmeet
```
Creates a 60-minute meeting titled "Quick Meeting"

### Advanced Usage

```
/gmeet Team Standup 30m
```
Creates a 30-minute meeting titled "Team Standup"

```
/gmeet Weekly Sync 2h
```
Creates a 2-hour meeting titled "Weekly Sync"

### Duration Formats

- `30m` - 30 minutes
- `1h` - 1 hour
- `2h30m` - 2 hours 30 minutes
- `90m` - 90 minutes

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SLACK_BOT_TOKEN` | Slack bot token (starts with xoxb-) | Yes |
| `SLACK_SIGNING_SECRET` | Slack app signing secret | Yes |
| `SLACK_APP_TOKEN` | Slack app-level token (starts with xapp-) | Yes |
| `GOOGLE_CREDENTIALS_FILE` | Path to Google credentials JSON | Yes |
| `GOOGLE_TOKEN_FILE` | Path to Google token JSON | Yes |
| `BOT_USER_ID` | Slack bot user ID | No |

### Google Calendar Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Calendar API
4. Create OAuth2 credentials (Desktop application)
5. Download the credentials file as `credentials.json`
6. Place it in the `credentials/` directory

### Slack App Setup

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Create a new app
3. Configure OAuth & Permissions with required scopes:
   - `chat:write`
   - `commands`
   - `app_mentions:read`
   - `im:read`
   - `im:write`
4. Create a slash command `/gmeet`
5. Install the app to your workspace

## Project Structure

```
gmeetslack/
├── main.py                 # Main application entry point
├── config.py              # Configuration management
├── slack_handlers.py      # Slack bot event handlers
├── google_calendar.py     # Google Calendar API integration
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
├── docker-compose.prod.yml # Production configuration
├── .dockerignore         # Docker ignore file
├── env.example           # Environment variables template
├── scripts/              # Helper scripts
│   ├── build.sh
│   ├── run.sh
│   └── stop.sh
├── credentials/          # Google credentials (you add this)
└── logs/                # Application logs
```

## Troubleshooting

### Common Issues

1. **Container won't start**
   - Check if `.env` file exists and has correct values
   - Verify `credentials.json` is in the `credentials/` directory
   - Check Docker logs: `docker-compose logs`

2. **"could not locate runnable browser" error**
   - Run `python setup_auth.py` first to set up authentication
   - Complete the OAuth flow in your browser
   - Copy the generated `token.json` to your container
   - For Docker: Mount the `credentials/` directory as a volume

3. **Authentication errors**
   - Verify Slack tokens are correct
   - Check Google credentials file
   - Ensure Google Calendar API is enabled
   - Run `python setup_auth.py` to set up Google OAuth

4. **Permission denied**
   - Make sure scripts are executable: `chmod +x scripts/*.sh`
   - Check file permissions in the `credentials/` directory

### Logs

```bash
# View all logs
docker-compose logs

# View logs for specific service
docker-compose logs gmeetslack-bot

# Follow logs in real-time
docker-compose logs -f
```

## Security

- Never commit `.env` or `credentials.json` files
- Use environment variables for sensitive data
- Regularly rotate your Slack tokens
- Monitor bot usage and permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Slack and Google API documentation
3. Check the console logs for error messages