import discord
from discord.ext import commands

# Imposta il canale di testo dove mandare le notifiche (metti l'ID)
TEXT_CHANNEL_ID = 1404501486939144324  # Sostituisci con ID del canale testuale

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connesso come {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    # Caso: utente entra in un canale vocale
    if before.channel is None and after.channel is not None:
        channel = bot.get_channel(TEXT_CHANNEL_ID)
        if channel:
            await channel.send(f"🔊 **{member.display_name}** si è collegato a **{after.channel.name}**")
    # Caso: utente esce da un canale vocale
    elif before.channel is not None and after.channel is None:
        channel = bot.get_channel(TEXT_CHANNEL_ID)
        if channel:
            await channel.send(f"🔊 **{member.display_name}** si è disconnesso da **{before.channel.name}**")

# Avvia il bot (incolla qui il tuo token)
bot.run("IL_TUO_TOKEN_DEL_BOT")