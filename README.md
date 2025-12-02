# Discord Bot Voice Monitor

A Discord bot that monitors voice channel activity and sends real-time notifications.

## 🚀 Features

- Monitors connections/disconnections from voice channels
- Real-time notifications in a text channel
- Channel change tracking
- Status and ping commands
- Automatic reconnection
- Lightweight

## 🛠️ Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/LeoAlb208/Voice-Chat-Alert.git
cd Voice-Chat-Alert
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configuration (Local)
Create a `.env` file based on `.env.example`:
```env
DISCORD_BOT_TOKEN=your_bot_token_here
TEXT_CHANNEL_ID=your_channel_id_here
```
The bot reads environment variables from `.env` locally using `python-dotenv`.

### 4. Start the bot
```bash
python main.py
```

## 🔧 Discord Developer Portal

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and add a Bot
3. Copy the bot token and put it in the `.env` file (local) or in Discloud App Variables (hosting)
4. Enable privileged intents on the bot:
   - Server Members Intent
   - Message Content Intent
   - Presence/Voice State as needed

## 📝 Commands

- `!ping` — Checks the bot's latency
- `!status` — Shows basic bot information

## 🌐 Hosting on Discloud (VS Code Extension)

This project is prepared for deployment via the Discloud VS Code extension using the included `discloud.config`.

Important:
- Deployment goes to the Discloud account currently authenticated in your VS Code Discloud extension.
- To deploy to your own account, make sure you are logged into your own Discloud account in the extension before uploading.

Steps:
1. Install and log into the Discloud VS Code extension using your Discloud account.
2. Open the project in VS Code.
3. Click “Upload to Discloud” (bottom-left in the status bar).
4. Confirm the upload. The app will be created under the account you’re logged into.
5. After the upload, open your app in the Discloud dashboard and set App Variables:
   - `DISCORD_BOT_TOKEN` — required
   - `TEXT_CHANNEL_ID` — required
6. Optionally choose the application image directly in the Discloud dashboard.

Notes:
- `discloud.config` is included and used by the extension; users do not need to create their own.
- `.discloudignore` has been removed because it is not needed for this workflow.
- The bot does not use `.env` on Discloud; it reads values from App Variables.

## 📋 Environment Variables

| Variable | Description | Required |
|---------|-------------|----------|
| `DISCORD_BOT_TOKEN` | Discord bot token | ✅ |
| `TEXT_CHANNEL_ID` | ID of the text channel for notifications | ✅ |

## 🔒 Security

- Do not commit your bot token.
- Use environment variables (.env locally, App Variables on Discloud).
- `.env` is ignored by Git.

## 🧰 Implementation Notes

- Configuration is loaded strictly from environment variables in `main.py` (no `config.json` fallback).
- `TEXT_CHANNEL_ID` must be an integer.
- Intents are configured in code; enable any privileged intents in the Developer Portal.

## 📞 Support

Open an issue on GitHub if you encounter problems or have questions.