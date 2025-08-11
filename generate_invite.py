#!/usr/bin/env python3
"""
Script to generate Discord bot invite link
"""

# Your bot's client ID (this is the Bot ID from the logs)
BOT_CLIENT_ID = "1404503977160081418"

# Required permissions for voice channel monitoring
# These are the permission values that need to be added together
PERMISSIONS = {
    'view_channels': 1024,          # View channels
    'send_messages': 2048,          # Send messages  
    'read_message_history': 65536,  # Read message history
    'connect': 1048576,             # Connect to voice channels
    'use_voice_activation': 2097152 # Use voice activity
}

# Calculate total permissions value
total_permissions = sum(PERMISSIONS.values())

# Generate the invite URL (simplified format for bot invites)
invite_url = f"https://discord.com/oauth2/authorize?client_id={BOT_CLIENT_ID}&permissions={total_permissions}&scope=bot"

print("Discord Bot Invite Link Generator")
print("=" * 40)
print(f"Bot Client ID: {BOT_CLIENT_ID}")
print(f"Required Permissions: {total_permissions}")
print("\nPermissions included:")
for perm_name, perm_value in PERMISSIONS.items():
    print(f"  - {perm_name.replace('_', ' ').title()}: {perm_value}")

print("\n" + "=" * 40)
print("INVITE LINK:")
print(invite_url)
print("\n" + "=" * 40)

print("\nInstructions:")
print("1. Copy the invite link above")
print("2. Paste it in your browser")
print("3. Select the Discord server where you're an admin")
print("4. Confirm the permissions")
print("5. Click 'Authorize'")

print("\nAfter inviting the bot:")
print("- The bot will appear in your server's member list")
print("- It will start monitoring voice channel activity")
print("- Notifications will be sent to the configured text channel")