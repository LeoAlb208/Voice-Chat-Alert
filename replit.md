# Discord Voice Monitor Bot

## Overview

This is a Discord bot that monitors voice channel activity and sends notifications to a designated text channel when users join or leave voice channels. The bot includes a Flask web server for health monitoring and status checks, making it suitable for deployment on cloud platforms that require a web interface to keep the service alive.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Architecture
- **Discord.py Framework**: Uses the discord.py library with command extension for bot functionality
- **Event-Driven Design**: Responds to Discord voice state changes through event handlers
- **Asynchronous Processing**: Built on asyncio for handling multiple Discord events concurrently

### Web Server Component
- **Flask Application**: Lightweight web server running on port 5000 for health checks
- **Threading Model**: Web server runs in a separate daemon thread to avoid blocking the Discord bot
- **Health Endpoints**: Provides `/ping` and `/health` endpoints for monitoring services

### Configuration Management
- **Environment Variables**: Bot token and channel IDs configured through environment variables
- **Fallback Defaults**: Default text channel ID provided as fallback configuration
- **Error Handling**: Validates required environment variables at startup

### Logging System
- **Dual Output**: Logs to both file (`bot.log`) and console for debugging and monitoring
- **Structured Logging**: Timestamped logs with appropriate log levels
- **Werkzeug Suppression**: Flask's default logging disabled to reduce noise

### Discord Integration
- **Voice State Monitoring**: Tracks user voice channel join/leave events
- **Text Notifications**: Sends formatted messages to configured text channel
- **Bot Presence**: Sets custom activity status to indicate monitoring functionality
- **Intents Configuration**: Enables member and voice state intents for proper event handling

## External Dependencies

### Core Dependencies
- **Discord.py**: Python library for Discord bot development and API interaction
- **Flask**: Lightweight web framework for health monitoring endpoints

### Discord API
- **Bot Token**: Requires Discord bot token for authentication
- **Voice State Events**: Monitors voice_state_update events from Discord
- **Text Channel API**: Sends messages to designated text channels

### Runtime Environment
- **Python 3.x**: Core runtime environment
- **Environment Variables**: Configuration through `DISCORD_BOT_TOKEN` and `TEXT_CHANNEL_ID`
- **File System**: Writes logs to `bot.log` file for persistence

### Web Technologies
- **Bootstrap 5**: Frontend CSS framework for web interface styling
- **Font Awesome**: Icon library for web interface elements
- **HTML Templates**: Flask template rendering for status page