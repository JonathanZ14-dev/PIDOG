#!/usr/bin/env python3
"""Record and transcribe one sentence without initializing PiDog motion."""

from __future__ import annotations

import argparse
from pathlib import Path

from speech_input import OfflineSpeechInput


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Record a WAV file, then transcribe it locally with Vosk."
    )
    parser.add_argument("--language", default="en-us")
    parser.add_argument("--rate", type=int, default=16_000)
    parser.add_argument("--seconds", type=float, default=6.0)
    parser.add_argument("--device", default=None)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/tmp/buck-vosk-last.wav"),
    )
    args = parser.parse_args()

    if args.seconds <= 0:
        parser.error("--seconds must be greater than zero")

    device: int | str | None = args.device
    if isinstance(device, str) and device.isdecimal():
        device = int(device)

    print(f"Loading the Vosk {args.language!r} model...")
    print("The first run downloads the small language model; later runs are offline.")
    speech = OfflineSpeechInput(language=args.language, sample_rate=args.rate)
    print(f"Model: {speech.model_name}")
    print(
        f"Recording {args.seconds:g} seconds. Wait one second, say one sentence, "
        "then pause."
    )
    result = speech.record_and_transcribe(
        seconds=args.seconds,
        output=args.output,
        device=device,
    )

    print(f"Saved recording: {result.recording_path}")
    print(f"Peak: {result.peak:.4f} ({result.peak_dbfs:.1f} dBFS)")
    print(f"RMS:  {result.rms:.4f} ({result.rms_dbfs:.1f} dBFS)")
    print(f"Clipped samples: {result.clipped_percent:.3f}%")
    print(f"Final transcript: {result.transcript!r}")
    print(f"Replay with: aplay -D default {result.recording_path}")


if __name__ == "__main__":
    main()
