import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Google Cloud TTS
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# ElevenLabs API
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Available TTS Models
TTS_MODELS = {
    "google": "Google TTS",
    "elevenlabs": "ElevenLabs"
}

# Google TTS Voices (Hindi & English)
GOOGLE_VOICES = {
    "hi-IN-Standard-A": "Hindi Female (Standard A)",
    "hi-IN-Standard-B": "Hindi Male (Standard B)",
    "hi-IN-Standard-C": "Hindi Female (Standard C)",
    "hi-IN-Standard-D": "Hindi Male (Standard D)",
    "hi-IN-Wavenet-A": "Hindi Female (Wavenet A)",
    "hi-IN-Wavenet-B": "Hindi Male (Wavenet B)",
    "hi-IN-Wavenet-C": "Hindi Female (Wavenet C)",
    "hi-IN-Wavenet-D": "Hindi Male (Wavenet D)",
    "en-US-Standard-A": "English US Female (Standard A)",
    "en-US-Standard-B": "English US Male (Standard B)",
    "en-US-Wavenet-A": "English US Female (Wavenet A)",
    "en-US-Wavenet-B": "English US Male (Wavenet B)",
    "en-IN-Standard-A": "English India Female (Standard A)",
    "en-IN-Standard-B": "English India Male (Standard B)",
    "en-IN-Wavenet-A": "English India Female (Wavenet A)",
    "en-IN-Wavenet-B": "English India Male (Wavenet B)",
}

# ElevenLabs Voices (Popular ones)
ELEVENLABS_VOICES = {
    "21m00Tcm4TlvDq8ikWAM": "Rachel (Female)",
    "AZnzlk1XvdvUeBnXmlld": "Domi (Female)",
    "EXAVITQu4vr4xnSDxMaL": "Bella (Female)",
    "ErXwobaYiN019PkySvjV": "Antoni (Male)",
    "MF3mGyEYCl7XYWbV9V6O": "Elli (Female)",
    "TxGEqnHWrfWFTfGW9XjX": "Josh (Male)",
    "VR6AewLTigWG4xSOukaG": "Arnold (Male)",
    "pNInz6obpgDQGcFmaJgB": "Adam (Male)",
    "yoZ06aMxZJJ28mfd3POQ": "Sam (Male)",
}

# Default Settings
DEFAULT_MODEL = "google"
DEFAULT_GOOGLE_VOICE = "hi-IN-Wavenet-A"
DEFAULT_ELEVENLABS_VOICE = "21m00Tcm4TlvDq8ikWAM"

# Audio Settings
AUDIO_FORMAT = "mp3"
SAMPLE_RATE = 24000
