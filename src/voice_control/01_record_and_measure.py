#!/usr/bin/env python3
"""Record a short microphone sample without initializing any PiDog hardware."""

from __future__ import annotations

import argparse
import math
import wave
from pathlib import Path

import numpy as np
import sounddevice as sd


def dbfs(value: float) -> float:
    """Convert a normalized amplitude (0.0 to 1.0) to decibels full scale."""
    if value <= 0:
        return float("-inf")
    return 20 * math.log10(value)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Record Buck's microphone and report its signal level."
    )
    parser.add_argument("--seconds", type=float, default=4.0)
    parser.add_argument("--rate", type=int, default=16_000)
    parser.add_argument("--device", default=None)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/tmp/buck-microphone-test.wav"),
    )
    args = parser.parse_args()

    if args.seconds <= 0:
        parser.error("--seconds must be greater than zero")

    device: int | str | None = args.device
    if isinstance(device, str) and device.isdecimal():
        device = int(device)

    frames = round(args.seconds * args.rate)
    sd.check_input_settings(
        device=device,
        channels=1,
        dtype="int16",
        samplerate=args.rate,
    )

    print(f"Recording {args.seconds:g} seconds. Speak normally now...")
    audio = sd.rec(
        frames,
        samplerate=args.rate,
        channels=1,
        dtype="int16",
        device=device,
    )
    sd.wait()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(args.output), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(args.rate)
        wav.writeframes(audio.tobytes())

    normalized = audio.astype(np.float64).reshape(-1) / 32768.0
    peak = float(np.max(np.abs(normalized))) if normalized.size else 0.0
    rms = float(np.sqrt(np.mean(np.square(normalized)))) if normalized.size else 0.0
    clipped = float(np.mean(np.abs(audio.reshape(-1)) >= 32760) * 100)

    print(f"Saved: {args.output}")
    print(f"Format: {args.rate} Hz, mono, signed 16-bit PCM")
    print(f"Peak: {peak:.4f} ({dbfs(peak):.1f} dBFS)")
    print(f"RMS:  {rms:.4f} ({dbfs(rms):.1f} dBFS)")
    print(f"Clipped samples: {clipped:.3f}%")

    if peak == 0:
        print("Result: silence; check the microphone route or capture mute.")
    elif clipped > 0.1:
        print("Result: the signal is clipping; lower the capture level.")
    elif dbfs(rms) < -45:
        print("Result: a signal exists but is very quiet.")
    else:
        print("Result: the microphone captured a usable signal.")


if __name__ == "__main__":
    main()
