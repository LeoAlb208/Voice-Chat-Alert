# Discord Bot Voice Monitor

Un bot Discord che monitora l'attività dei canali vocali e invia notifiche in tempo reale.

## 🚀 Caratteristiche

- ✅ Monitora connessioni/disconnessioni dai canali vocali
- ✅ Notifiche automatiche in un canale di testo
- ✅ Tracking cambio canale
- ✅ Comandi per controllo stato bot
- ✅ Web server integrato per monitoring
- ✅ Riconnessione automatica

## 🛠️ Setup

### 1. Clona il repository
```bash
git clone <url-del-tuo-repo>
cd Voice-Chat-Alert
```

### 2. Installa le dipendenze
```bash
pip install -r requirements.txt
```

### 3. Configurazione
Crea un file `.env` con le seguenti variabili:
```env
DISCORD_BOT_TOKEN=your_bot_token_here
TEXT_CHANNEL_ID=your_channel_id_here
```

### 4. Avvia il bot
```bash
python main.py
```

## 🔧 Configurazione Discord Bot

1. Vai su [Discord Developer Portal](https://discord.com/developers/applications)
2. Crea una nuova applicazione
3. Vai nella sezione "Bot" e crea un bot
4. Copia il token e mettilo nel file `.env`
5. Abilita i seguenti intents:
   - Message Content Intent
   - Server Members Intent

## 📝 Comandi

- `!ping` - Controlla la latenza del bot
- `!status` - Mostra informazioni dettagliate del bot

## 🌐 Deploy

### Railway (Consigliato)
1. Fai push su GitHub
2. Connetti il repository su Railway
3. Aggiungi le variabili d'ambiente
4. Deploy automatico

### Altre piattaforme
- Render
- Fly.io  
- Heroku alternatives

## 📋 Variabili d'Ambiente

| Variabile | Descrizione | Obbligatorio |
|-----------|-------------|--------------|
| `DISCORD_BOT_TOKEN` | Token del bot Discord | ✅ |
| `TEXT_CHANNEL_ID` | ID del canale per le notifiche | ✅ |

## 🔒 Sicurezza

- ⚠️ **NON committare mai il token del bot**
- ✅ Usa sempre variabili d'ambiente
- ✅ Il file `.env` è nel `.gitignore`

## 📞 Supporto

Per problemi o domande, apri un'issue su GitHub.
