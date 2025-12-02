import discord
from discord.ext import commands
import os
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables from .env file (useful locally; Discloud uses app vars)
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('bot.log', maxBytes=1024 * 1024, backupCount=2),
        logging.StreamHandler()
    ]
)

# Load configuration from environment only (Discloud App Variables or local .env)
def load_config():
    """Load configuration from environment variables"""
    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    text_channel_id = os.getenv('TEXT_CHANNEL_ID')

    if not bot_token:
        logging.error("DISCORD_BOT_TOKEN not found. Set it in .env (local) or Discloud App Variables.")
        raise ValueError("DISCORD_BOT_TOKEN not found in environment variables")

    if not text_channel_id:
        logging.error("TEXT_CHANNEL_ID not found. Set it in .env (local) or Discloud App Variables.")
        raise ValueError("TEXT_CHANNEL_ID not found in environment variables")

    # Ensure channel id is int
    try:
        channel_id_int = int(text_channel_id)
    except ValueError:
        logging.error(f"TEXT_CHANNEL_ID must be an integer, got '{text_channel_id}'")
        raise

    return bot_token, channel_id_int

# Get configuration
BOT_TOKEN, TEXT_CHANNEL_ID = load_config()

# Configure intents
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents, max_messages=100)  # Limit cached messages

@bot.event
async def on_ready():
    """Event triggered when bot successfully connects to Discord"""
    if bot.user:
        logging.info(f"✅ Bot connected as {bot.user}")
        logging.info(f"Bot ID: {bot.user.id}")
        logging.info(f"Connected to {len(bot.guilds)} server(s)")
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="voice channels 👀"
        )
    )

@bot.event
async def on_voice_state_update(member, before, after):
    """Event triggered when a user's voice state changes"""
    try:
        # Skip bot users
        if member.bot:
            return
            
        channel = bot.get_channel(TEXT_CHANNEL_ID)
        if not channel:
            logging.error(f"Text channel with ID {TEXT_CHANNEL_ID} not found")
            return
        
        # Type check to ensure it's a text channel
        if not hasattr(channel, 'send'):
            logging.error(f"The channel with ID {TEXT_CHANNEL_ID} is not a text channel")
            return

        # User joins a voice channel
        if before.channel is None and after.channel is not None:
            message = f"🔊 **{member.display_name}** has connected to **{after.channel.name}**"
            await channel.send(message)
            logging.info(f"{member.display_name} has connected to {after.channel.name}")
            
        # User leaves a voice channel
        elif before.channel is not None and after.channel is None:
            message = f"🔇 **{member.display_name}** has disconnected from **{before.channel.name}**"
            await channel.send(message)
            logging.info(f"{member.display_name} has disconnected from {before.channel.name}")
            
        # User switches voice channels
        elif before.channel is not None and after.channel is not None and before.channel != after.channel:
            message = f"🔄 **{member.display_name}** has moved from **{before.channel.name}** to **{after.channel.name}**"
            await channel.send(message)
            logging.info(f"{member.display_name} has moved from {before.channel.name} to {after.channel.name}")
            
    except Exception as e:
        logging.error(f"Error during voice state update: {e}")

@bot.event
async def on_disconnect():
    """Event triggered when bot disconnects"""
    logging.warning("⚠️ Bot disconnected from Discord")

@bot.event
async def on_resumed():
    """Event triggered when bot resumes connection"""
    logging.info("🔄 Connection resumed")

@bot.event
async def on_error(event, *args, **kwargs):
    """Global error handler"""
    logging.error(f"Error in event {event}: {args}, {kwargs}")

@bot.command(name='status')
async def status_command(ctx):
    """Command to check bot status"""
    try:
        embed = discord.Embed(
            title="📊 Bot Status",
            color=0x00ff00,
            description="The bot is online and working!"
        )
        embed.add_field(
            name="🏓 Latency", 
            value=f"{round(bot.latency * 1000)}ms", 
            inline=True
        )
        embed.add_field(
            name="🔗 Servers", 
            value=f"{len(bot.guilds)}", 
            inline=True
        )
        embed.add_field(
            name="👥 Users", 
            value=f"{len(set(bot.get_all_members()))}", 
            inline=True
        )
        
        await ctx.send(embed=embed)
        logging.info(f"Status command executed by {ctx.author}")
        
    except Exception as e:
        logging.error(f"Error in status command: {e}")
        await ctx.send("❌ Error while retrieving bot information")

@bot.command(name='ping')
async def ping_command(ctx):
    """Simple ping command"""
    try:
        latency = round(bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latency: {latency}ms")
        logging.info(f"Ping command executed by {ctx.author} - Latency: {latency}ms")
    except Exception as e:
        logging.error(f"Error in ping command: {e}")

async def main():
    """Main function to start the bot with error handling"""
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            logging.info(f"Attempting to connect #{retry_count + 1}")
            await bot.start(BOT_TOKEN)
            break
            
        except discord.LoginFailure:
            logging.error("❌ Invalid bot token")
            break
            
        except discord.ConnectionClosed:
            retry_count += 1
            if retry_count < max_retries:
                wait_time = min(2 ** retry_count, 300)
                logging.warning(f"⚠️ Connection lost. Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                logging.error("❌ Maximum number of retries reached")
                
        except Exception as e:
            logging.error(f"❌ Unexpected error: {e}")
            retry_count += 1
            if retry_count < max_retries:
                await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Bot stopped manually")
    except Exception as e:
        logging.error(f"❌ Fatal error: {e}")
