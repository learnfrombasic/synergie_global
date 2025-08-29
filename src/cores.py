import io
from typing import Dict, List

import numpy as np
import sounddevice as sd
from groq import Groq
from scipy.io.wavfile import write as wav_write

from src.configs import settings
from src.commons import setup_logger

logger = setup_logger(settings.APP_NAME)


def record_audio(seconds: float = 3.0) -> np.ndarray:
    logger.debug(f"(Recording {seconds:.1f}s… speak now)")
    audio = sd.rec(
        int(seconds * settings.SAMPLE_RATE),
        samplerate=settings.SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    audio = audio.flatten()
    # Normalize
    audio = audio / max(1e-9, np.max(np.abs(audio)))
    return (audio * 32767).astype(np.int16)


def stt_groq(client: Groq, audio_wav: bytes) -> str:
    # Groq transcription expects a file-like obj
    resp = client.audio.transcriptions.create(
        model=settings.GROQ_STT_MODEL, file=("input.wav", io.BytesIO(audio_wav))
    )
    # Groq returns { "text": "..."}
    return getattr(resp, "text", "").strip()


def tts_say(engine, text: str):
    engine.say(text)
    engine.runAndWait()


def chat_groq(client: Groq, history: List[Dict[str, str]]) -> str:
    resp = client.chat.completions.create(
        model=settings.GROQ_MODEL_NAME,
        messages=history,
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()
