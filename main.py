import discord
from discord.ext import commands
import os
import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

# Get configuration from environment variables
TEXT_CHANNEL_ID = int(os.getenv('TEXT_CHANNEL_ID', '1404522797765492858'))
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is required")

# Configure intents
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """Event triggered when bot successfully connects to Discord"""
    if bot.user:
        logging.info(f"✅ Bot connesso come {bot.user}")
        logging.info(f"Bot ID: {bot.user.id}")
        logging.info(f"Connesso a {len(bot.guilds)} server(s)")
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="i canali vocali 👀"
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
            logging.error(f"Canale di testo con ID {TEXT_CHANNEL_ID} non trovato")
            return
        
        # Type check to ensure it's a text channel
        if not hasattr(channel, 'send'):
            logging.error(f"Il canale con ID {TEXT_CHANNEL_ID} non è un canale di testo")
            return

        # User joins a voice channel
        if before.channel is None and after.channel is not None:
            message = f"🔊 **{member.display_name}** si è collegato a **{after.channel.name}**"
            await channel.send(message)
            logging.info(f"{member.display_name} si è collegato a {after.channel.name}")
            
        # User leaves a voice channel
        elif before.channel is not None and after.channel is None:
            message = f"🔇 **{member.display_name}** si è disconnesso da **{before.channel.name}**"
            await channel.send(message)
            logging.info(f"{member.display_name} si è disconnesso da {before.channel.name}")
            
        # User switches voice channels
        elif before.channel is not None and after.channel is not None and before.channel != after.channel:
            message = f"🔄 **{member.display_name}** si è spostato da **{before.channel.name}** a **{after.channel.name}**"
            await channel.send(message)
            logging.info(f"{member.display_name} si è spostato da {before.channel.name} a {after.channel.name}")
            
    except Exception as e:
        logging.error(f"Errore durante l'aggiornamento dello stato vocale: {e}")

@bot.event
async def on_disconnect():
    """Event triggered when bot disconnects"""
    logging.warning("⚠️ Bot disconnesso da Discord")

@bot.event
async def on_resumed():
    """Event triggered when bot resumes connection"""
    logging.info("🔄 Connessione ripristinata")

@bot.event
async def on_error(event, *args, **kwargs):
    """Global error handler"""
    logging.error(f"Errore nell'evento {event}: {args}, {kwargs}")

@bot.command(name='status')
async def status_command(ctx):
    """Command to check bot status"""
    try:
        embed = discord.Embed(
            title="📊 Stato del Bot",
            color=0x00ff00,
            description="Il bot è online e funzionante!"
        )
        embed.add_field(
            name="🏓 Latenza", 
            value=f"{round(bot.latency * 1000)}ms", 
            inline=True
        )
        embed.add_field(
            name="🔗 Server", 
            value=f"{len(bot.guilds)}", 
            inline=True
        )
        embed.add_field(
            name="👥 Utenti", 
            value=f"{len(set(bot.get_all_members()))}", 
            inline=True
        )
        
        await ctx.send(embed=embed)
        logging.info(f"Comando status eseguito da {ctx.author}")
        
    except Exception as e:
        logging.error(f"Errore nel comando status: {e}")
        await ctx.send("❌ Errore durante il recupero delle informazioni del bot")

@bot.command(name='ping')
async def ping_command(ctx):
    """Simple ping command"""
    try:
        latency = round(bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latenza: {latency}ms")
        logging.info(f"Comando ping eseguito da {ctx.author} - Latenza: {latency}ms")
    except Exception as e:
        logging.error(f"Errore nel comando ping: {e}")

async def main():
    """Main function to start the bot with error handling"""
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            logging.info(f"Tentativo di connessione #{retry_count + 1}")
            await bot.start(BOT_TOKEN)
            break
            
        except discord.LoginFailure:
            logging.error("❌ Token del bot non valido")
            break
            
        except discord.ConnectionClosed:
            retry_count += 1
            if retry_count < max_retries:
                wait_time = min(2 ** retry_count, 300)
                logging.warning(f"⚠️ Connessione persa. Riprovo tra {wait_time} secondi...")
                await asyncio.sleep(wait_time)
            else:
                logging.error("❌ Massimo numero di tentativi raggiunto")
                
        except Exception as e:
            logging.error(f"❌ Errore imprevisto: {e}")
            retry_count += 1
            if retry_count < max_retries:
                await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Bot fermato manualmente")
    except Exception as e:
        logging.error(f"❌ Errore fatale: {e}")
