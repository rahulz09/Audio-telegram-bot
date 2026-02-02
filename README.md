# Audio Telegram Bot

A Telegram bot that converts YouTube scripts to audio using Google TTS and ElevenLabs APIs.

## Features

- Convert text/scripts to audio
- Multiple TTS models: Google TTS & ElevenLabs
- Multiple voice options (Hindi & English)
- Fixed menu for easy navigation
- Voice selection menu
- Settings menu
- Model selection menu

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Audio-telegram-bot.git
cd Audio-telegram-bot
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` file:

```env
# Telegram Bot Token (Get from @BotFather)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Google Cloud TTS (Path to service account JSON file)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google-credentials.json

# ElevenLabs API Key (Get from elevenlabs.io)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### 5. Get API Keys

#### Telegram Bot Token
1. Open Telegram and search for @BotFather
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the token provided

#### Google Cloud TTS
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Cloud Text-to-Speech API"
4. Create a service account and download JSON key
5. Set the path to JSON file in `.env`

#### ElevenLabs API
1. Go to [ElevenLabs](https://elevenlabs.io/)
2. Create an account
3. Go to Profile Settings > API Keys
4. Generate and copy your API key

### 6. Run the bot

```bash
python bot.py
```

## Usage

1. Start the bot with `/start` command
2. Use the menu buttons:
   - **Voice Select** - Choose voice for current model
   - **Settings** - View current settings
   - **Model Select** - Choose between Google TTS and ElevenLabs
   - **Help** - View help guide
3. Paste your script text
4. Receive audio file!

## Available Voices

### Google TTS
- Hindi voices (Standard & Wavenet)
- English US voices (Standard & Wavenet)
- English India voices (Standard & Wavenet)

### ElevenLabs
- Rachel, Domi, Bella (Female)
- Antoni, Josh, Arnold, Adam, Sam (Male)

## Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/settings` - View current settings
- `/voice` - Select voice
- `/model` - Select TTS model

## Project Structure

```
Audio-telegram-bot/
├── bot.py              # Main bot file
├── config.py           # Configuration and settings
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment file
├── .gitignore          # Git ignore file
├── README.md           # This file
└── services/
    ├── __init__.py
    ├── google_tts.py   # Google TTS service
    └── elevenlabs_tts.py # ElevenLabs service
```

## License

MIT License
