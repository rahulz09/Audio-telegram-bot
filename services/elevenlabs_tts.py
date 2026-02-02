import tempfile
from elevenlabs import ElevenLabs

import config


class ElevenLabsTTSService:
    """ElevenLabs Text-to-Speech Service"""

    def __init__(self):
        self.client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)

    async def synthesize(self, text: str, voice_id: str) -> str:
        """
        Convert text to speech using ElevenLabs API

        Args:
            text: Text to convert to speech
            voice_id: Voice ID from config.ELEVENLABS_VOICES

        Returns:
            Path to the generated audio file
        """
        # Generate audio using ElevenLabs
        audio_generator = self.client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id="eleven_multilingual_v2"
        )

        # Save audio to temp file
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=f".{config.AUDIO_FORMAT}"
        )

        # Write audio chunks to file
        for chunk in audio_generator:
            temp_file.write(chunk)

        temp_file.close()

        return temp_file.name

    def get_available_voices(self) -> dict:
        """Return available ElevenLabs voices"""
        return config.ELEVENLABS_VOICES
