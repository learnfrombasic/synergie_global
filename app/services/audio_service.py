import io
from typing import Optional

import numpy as np
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write as wav_write

from ..configs.settings import settings


class AudioService:
    """Handles all audio input/output operations."""

    def __init__(self):
        self.sample_rate = settings.SAMPLE_RATE
        self.recording_duration = settings.RECORDING_DURATION
        self.push_to_talk = settings.PUSH_TO_TALK

        # Initialize TTS engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty("rate", settings.TTS_RATE)

    def record_audio(self, duration: Optional[float] = None) -> bytes:
        """Record audio from the microphone.

        Args:
            duration: Recording duration in seconds. If None, uses default from settings.

        Returns:
            bytes: WAV audio data
        """
        duration = duration or self.recording_duration
        print(f"(Recording {duration:.1f}s… speak now)")

        # Record audio
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()

        # Process audio
        audio = audio.flatten()
        audio = audio / max(1e-9, np.max(np.abs(audio)))  # Normalize
        audio = (audio * 32767).astype(np.int16)  # Convert to 16-bit PCM

        # Convert to WAV bytes
        buf = io.BytesIO()
        wav_write(buf, self.sample_rate, audio)
        return buf.getvalue()

    def text_to_speech(self, text: str, wait: bool = True) -> None:
        """Convert text to speech.

        Args:
            text: The text to speak
            wait: If True, blocks until speech is complete
        """
        self.tts_engine.say(text)
        if wait:
            self.tts_engine.runAndWait()

    def play_audio(self, audio_data: bytes) -> None:
        """Play audio data.

        Args:
            audio_data: WAV audio data
        """
        # TODO: Implement audio playback if needed
        pass

    def __del__(self):
        """Clean up resources."""
        try:
            self.tts_engine.stop()
        except:
            pass
