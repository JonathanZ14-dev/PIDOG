"""Reusable offline microphone capture and Vosk transcription."""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
import wave

import numpy as np
import sounddevice as sd


def dbfs(value: float) -> float:
    """Convert normalized amplitude to decibels relative to digital full scale."""
    if value <= 0:
        return float("-inf")
    return 20 * math.log10(value)


@dataclass(frozen=True)
class SpeechResult:
    transcript: str
    recording_path: Path
    peak: float
    rms: float
    clipped_percent: float

    @property
    def peak_dbfs(self) -> float:
        return dbfs(self.peak)

    @property
    def rms_dbfs(self) -> float:
        return dbfs(self.rms)


class OfflineSpeechInput:
    """Own the Vosk model and turn one fixed recording into text."""

    def __init__(self, language: str = "en-us", sample_rate: int = 16_000):
        # This is only the speech wrapper. It does not initialize Pidog.
        from pidog.stt import Vosk

        self.language = language
        self.sample_rate = sample_rate
        self._vosk = Vosk(language=language, samplerate=sample_rate)

    @property
    def model_name(self) -> str:
        return self._vosk.get_model_name(self.language)

    def record_and_transcribe(
        self,
        *,
        seconds: float = 6.0,
        output: Path = Path("/tmp/buck-vosk-last.wav"),
        device: int | str | None = None,
    ) -> SpeechResult:
        if seconds <= 0:
            raise ValueError("seconds must be greater than zero")

        frames = round(seconds * self.sample_rate)
        sd.check_input_settings(
            device=device,
            channels=1,
            dtype="int16",
            samplerate=self.sample_rate,
        )
        audio = sd.rec(
            frames,
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            device=device,
        )
        sd.wait()

        output.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(output), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            wav.writeframes(audio.tobytes())

        normalized = audio.astype(np.float64).reshape(-1) / 32768.0
        peak = float(np.max(np.abs(normalized))) if normalized.size else 0.0
        rms = (
            float(np.sqrt(np.mean(np.square(normalized))))
            if normalized.size
            else 0.0
        )
        clipped = (
            float(
                np.mean(np.abs(audio.reshape(-1).astype(np.int32)) >= 32760)
                * 100
            )
            if audio.size
            else 0.0
        )

        raw = audio.tobytes()
        bytes_per_chunk = 4_000 * 2
        for start in range(0, len(raw), bytes_per_chunk):
            self._vosk.recognizer.AcceptWaveform(
                raw[start : start + bytes_per_chunk]
            )
        result = json.loads(self._vosk.recognizer.FinalResult())
        transcript = result.get("text", "").strip()
        # FinalResult() finishes one utterance. Reset the recognizer so this
        # OfflineSpeechInput instance can safely be reused by an active loop.
        self._vosk.recognizer.Reset()

        return SpeechResult(
            transcript=transcript,
            recording_path=output,
            peak=peak,
            rms=rms,
            clipped_percent=clipped,
        )
