#!/usr/bin/env python3
"""Recognize and perform exactly one guarded PiDog voice command."""

from __future__ import annotations

import argparse
from pathlib import Path
import time

from command_parser import parse_command
from movement_actions import MOTION_ACTIONS, perform_approved_action
from speech_input import OfflineSpeechInput


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", default="en-us")
    parser.add_argument("--rate", type=int, default=16_000)
    parser.add_argument("--seconds", type=float, default=6.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/tmp/buck-voice-move-last.wav"),
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="allow the approved command to reach PiDog",
    )
    parser.add_argument(
        "--i-have-calibrated",
        action="store_true",
        help="confirm official servo calibration is complete",
    )
    parser.add_argument(
        "--on-stand",
        action="store_true",
        help="confirm Buck is secure on the stand with clear leg space",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.seconds <= 0:
        print("Refusing to run: --seconds must be greater than zero.")
        return 2

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
    )
    decision = parse_command(heard.transcript)

    print(f"Transcript: {heard.transcript!r}")
    print(f"Decision:   {decision.action or 'NO ACTION'}")
    print(f"Reason:     {decision.reason}")

    if decision.action is None:
        print("No movement: the transcript did not match the allowlist.")
        return 1

    if decision.action == "stop":
        print("Stop acknowledged. This one-shot program has no active motion to stop.")
        return 0

    if decision.action not in MOTION_ACTIONS:
        print("No movement: the parsed action is not approved by the motion layer.")
        return 2

    if not args.execute:
        print("Dry run only. Add --execute after reviewing the decision.")
        return 0

    if not args.i_have_calibrated or not args.on_stand:
        print(
            "Refusing to move: use both --i-have-calibrated and --on-stand "
            "after physically checking Buck."
        )
        return 2

    print(f"Approved action: {decision.action}. Motion begins in 3 seconds.")
    for remaining in range(3, 0, -1):
        print(remaining, flush=True)
        time.sleep(1)

    # Import and initialize physical hardware only after every safety check.
    from pidog import Pidog

    dog = Pidog()
    try:
        time.sleep(0.5)
        perform_approved_action(dog, decision.action)
        print(f"Completed action: {decision.action}")
        return 0
    finally:
        dog.close()


if __name__ == "__main__":
    raise SystemExit(main())
