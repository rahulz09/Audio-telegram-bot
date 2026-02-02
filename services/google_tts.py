import os
import tempfile
from google.cloud import texttospeech

import config


class GoogleTTSService:
    """Google Cloud Text-to-Speech Service"""

    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def get_language_code(self, voice_name: str) -> str:
        """Extract language code from voice name"""
        # Voice names are like "hi-IN-Wavenet-A"
        parts = voice_name.split("-")
        if len(parts) >= 2:
            return f"{parts[0]}-{parts[1]}"
        return "hi-IN"

    async def synthesize(self, text: str, voice_name: str) -> str:
        """
        Convert text to speech using Google Cloud TTS

        Args:
            text: Text to convert to speech
            voice_name: Voice name from config.GOOGLE_VOICES

        Returns:
            Path to the generated audio file
        """
        # Set up the text input
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Get language code from voice name
        language_code = self.get_language_code(voice_name)

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name
        )

        # Select the audio encoding
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            sample_rate_hertz=config.SAMPLE_RATE
        )

        # Perform the text-to-speech request
        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # Save audio to temp file
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=f".{config.AUDIO_FORMAT}"
        )
        temp_file.write(response.audio_content)
        temp_file.close()

        return temp_file.name

    def get_available_voices(self) -> dict:
        """Return available Google TTS voices"""
        return config.GOOGLE_VOICES
