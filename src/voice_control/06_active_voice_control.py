#!/usr/bin/env python3
"""Continuously listen for guarded PiDog commands."""

from __future__ import annotations

import argparse
from pathlib import Path
import time

from command_parser import parse_active_command
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
        default=Path("/tmp/buck-active-command-last.wav"),
        help="WAV path overwritten on every listening round",
    )
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=0,
        help="stop after this many rounds; 0 means keep listening",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="allow approved commands to reach PiDog",
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


def validate_args(args: argparse.Namespace) -> str | None:
    if args.seconds <= 0:
        return "--seconds must be greater than zero"
    if args.max_rounds < 0:
        return "--max-rounds cannot be negative"
    if args.execute and (not args.i_have_calibrated or not args.on_stand):
        return (
            "physical mode requires both --i-have-calibrated and --on-stand "
            "after physically checking Buck"
        )
    return None


def main() -> int:
    args = parse_args()
    error = validate_args(args)
    if error:
        print(f"Refusing to run: {error}.")
        return 2

    mode = "PHYSICAL MOTION" if args.execute else "DRY RUN (no motion)"
    print(f"Mode: {mode}")
    print("Commands: sit, stand, lie down, or wag your tail.")
    print("Say 'stop' by itself, or press Ctrl+C, to exit.")
    print(f"Each listening round is {args.seconds:g} seconds.")
    print(f"Loading the offline Vosk {args.language!r} model...")
    speech = OfflineSpeechInput(language=args.language, sample_rate=args.rate)
    print(f"Model: {speech.model_name}")

    dog = None
    try:
        if args.execute:
            print("Buck will enter active mode in 3 seconds.")
            for remaining in range(3, 0, -1):
                print(remaining, flush=True)
                time.sleep(1)

            # Initialize motion hardware only after all safety checks pass.
            from pidog import Pidog

            dog = Pidog()
            time.sleep(0.5)

        round_number = 0
        while args.max_rounds == 0 or round_number < args.max_rounds:
            round_number += 1
            print(f"\nListening (round {round_number})...", flush=True)
            heard = speech.record_and_transcribe(
                seconds=args.seconds,
                output=args.output,
            )
            decision = parse_active_command(heard.transcript)

            print(f"Transcript: {heard.transcript!r}")
            print(
                f"Levels: peak {heard.peak_dbfs:.1f} dBFS, "
                f"RMS {heard.rms_dbfs:.1f} dBFS, "
                f"clipped {heard.clipped_percent:.3f}%"
            )
            print(f"Decision: {decision.action or 'NO ACTION'} ({decision.reason})")

            if decision.action == "stop":
                print("Stop acknowledged. Leaving active mode.")
                break
            if decision.action is None:
                print("No movement. Listening again...")
                continue
            if decision.action not in MOTION_ACTIONS:
                print("No movement: action rejected by the motion layer.")
                continue
            if dog is None:
                print(f"Dry run: would execute {decision.action!r}.")
                continue

            print(f"Executing: {decision.action}")
            perform_approved_action(dog, decision.action)
            print("Action complete. Listening again...")

        else:
            print("Maximum listening rounds reached.")
        return 0
    except KeyboardInterrupt:
        print("\nCtrl+C received. Leaving active mode.")
        return 0
    finally:
        if dog is not None:
            dog.close()
            print("PiDog hardware closed safely.")


if __name__ == "__main__":
    raise SystemExit(main())
