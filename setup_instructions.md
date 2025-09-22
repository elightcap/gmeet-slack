# Setup Instructions

This guide will walk you through setting up the Google Meet Slack Bot step by step.

## Step 1: Google Cloud Setup

### 1.1 Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name (e.g., "slack-meet-bot")
4. Click "Create"

### 1.2 Enable Google Calendar API
1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google Calendar API"
3. Click on it and press "Enable"

### 1.3 Create OAuth2 Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in required fields (App name, User support email, Developer contact)
   - Add your email to test users
4. For Application type, choose "Desktop application"
5. Give it a name (e.g., "Slack Meet Bot")
6. Click "Create"
7. Download the JSON file and rename it to `credentials.json`
8. Place `credentials.json` in your project directory

## Step 2: Slack App Setup

### 2.1 Create Slack App
1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App"
3. Choose "From scratch"
4. Enter app name (e.g., "Google Meet Bot")
5. Select your workspace
6. Click "Create App"

### 2.2 Configure OAuth & Permissions
1. In your app settings, go to "OAuth & Permissions"
2. Scroll down to "Scopes" and add these Bot Token Scopes:
   - `chat:write`
   - `commands`
   - `app_mentions:read`
   - `im:read`
   - `im:write`
3. Click "Install to Workspace"
4. Copy the "Bot User OAuth Token" (starts with `xoxb-`)

### 2.3 Create Slash Command
1. Go to "Slash Commands"
2. Click "Create New Command"
3. Fill in:
   - Command: `/meet`
   - Request URL: `https://your-domain.com/slack/events` (for now, use a placeholder)
   - Short Description: `Create a Google Meet meeting`
   - Usage Hint: `[title] [duration]`
4. Click "Save"

### 2.4 Get App Credentials
1. Go to "Basic Information"
2. Copy these values:
   - "Signing Secret" (starts with a long string)
   - "App-Level Token" (starts with `xapp-`)

## Step 3: Environment Configuration

### 3.1 Create Environment File
1. Copy `env.example` to `.env`:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` with your actual values:
   ```env
   SLACK_BOT_TOKEN=xoxb-your-actual-bot-token
   SLACK_SIGNING_SECRET=your-actual-signing-secret
   SLACK_APP_TOKEN=xapp-your-actual-app-token
   GOOGLE_CREDENTIALS_FILE=credentials.json
   GOOGLE_TOKEN_FILE=token.json
   BOT_USER_ID=U1234567890
   ```

### 3.2 Get Bot User ID (Optional)
1. In Slack, mention your bot: `@YourBotName`
2. The bot will respond with its user ID
3. Add this to your `.env` file

## Step 4: Install and Run

### 4.1 Install Dependencies
```bash
pip install -r requirements.txt
```

### 4.2 First Run (Authentication)
```bash
python main.py
```

On first run:
1. The bot will open your browser for Google authentication
2. Sign in with your Google account
3. Grant calendar permissions
4. A `token.json` file will be created automatically

### 4.3 Test the Bot
1. In Slack, type `/meet`
2. You should see a meeting created with a Google Meet link
3. Try variations like `/meet Team Standup 30m`

## Step 5: Deploy (Optional)

For production deployment:

### 5.1 Using a VPS/Cloud Server
1. Upload your code to the server
2. Install Python and dependencies
3. Set up environment variables
4. Run with a process manager like `systemd` or `supervisor`

### 5.2 Using Heroku
1. Create a `Procfile`:
   ```
   worker: python main.py
   ```
2. Deploy to Heroku
3. Set environment variables in Heroku dashboard
4. Scale the worker dyno

### 5.3 Using Docker
1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "main.py"]
   ```
2. Build and run the container

## Troubleshooting

### Common Issues

1. **"Invalid credentials"**
   - Check your `.env` file values
   - Ensure no extra spaces or quotes

2. **"Calendar API not enabled"**
   - Go back to Google Cloud Console
   - Enable the Calendar API

3. **"Slack command not working"**
   - Check that the slash command is installed
   - Verify bot permissions
   - Check bot is running

4. **"Google authentication failed"**
   - Delete `token.json` and try again
   - Check `credentials.json` is in the right place

### Getting Help

1. Check the console output for error messages
2. Verify all environment variables are set correctly
3. Test Google Calendar API access separately
4. Test Slack app permissions

## Security Best Practices

1. **Never commit sensitive files:**
   - Add `.env`, `credentials.json`, `token.json` to `.gitignore`
   - Use environment variables in production

2. **Rotate tokens regularly:**
   - Update Slack tokens periodically
   - Regenerate Google credentials if compromised

3. **Monitor usage:**
   - Check bot logs for unusual activity
   - Set up alerts for failed authentications

4. **Limit permissions:**
   - Only grant necessary Slack scopes
   - Use service accounts for Google APIs when possible
