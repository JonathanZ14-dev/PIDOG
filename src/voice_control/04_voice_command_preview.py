#!/usr/bin/env python3
"""Preview a spoken command decision without initializing or moving PiDog."""

from __future__ import annotations

import argparse
from pathlib import Path

from command_parser import parse_command
from speech_input import OfflineSpeechInput


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Record, transcribe, and safely preview one voice command."
    )
    parser.add_argument("--language", default="en-us")
    parser.add_argument("--rate", type=int, default=16_000)
    parser.add_argument("--seconds", type=float, default=6.0)
    parser.add_argument("--device", default=None)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/tmp/buck-command-preview.wav"),
    )
    args = parser.parse_args()

    if args.seconds <= 0:
        parser.error("--seconds must be greater than zero")

    device: int | str | None = args.device
    if isinstance(device, str) and device.isdecimal():
        device = int(device)

    print(f"Loading the offline Vosk {args.language!r} model...")
    speech = OfflineSpeechInput(language=args.language, sample_rate=args.rate)
    print(f"Model: {speech.model_name}")
    print(
        f"Recording {args.seconds:g} seconds. Wait one second, speak one command, "
        "then pause."
    )
    heard = speech.record_and_transcribe(
        seconds=args.seconds,
        output=args.output,
        device=device,
    )
    decision = parse_command(heard.transcript)

    print("\n--- Speech input ---")
    print(f"Saved recording: {heard.recording_path}")
    print(f"Peak: {heard.peak_dbfs:.1f} dBFS")
    print(f"RMS:  {heard.rms_dbfs:.1f} dBFS")
    print(f"Clipped samples: {heard.clipped_percent:.3f}%")
    print(f"Transcript: {heard.transcript!r}")

    print("\n--- Safety decision ---")
    print(f"Normalized: {decision.normalized_text!r}")
    print(f"Action:     {decision.action or 'NO ACTION'}")
    print(f"Reason:     {decision.reason}")
    print("Motion:     disabled in this lesson")
    print(f"Replay with: aplay -D default {heard.recording_path}")


if __name__ == "__main__":
    main()
