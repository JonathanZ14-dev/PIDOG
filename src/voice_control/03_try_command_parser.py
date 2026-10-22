#!/usr/bin/env python3
"""Try Buck's command parser without importing or moving PiDog hardware."""

from __future__ import annotations

import argparse

from command_parser import parse_command


DEMO_PHRASES = (
    "Sit down!",
    "Hello Buck, please stand up.",
    "Wag your tail",
    "Please stop moving",
    "Run into the kitchen",
    "Sit and then stand",
)


def show_result(text: str) -> None:
    result = parse_command(text)
    print(f"Heard:      {result.original_text!r}")
    print(f"Normalized: {result.normalized_text!r}")
    print(f"Decision:   {result.action or 'NO ACTION'}")
    print(f"Reason:     {result.reason}")
    print("Motion:     disabled in this lesson")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Map text to Buck's safe action allowlist without movement."
    )
    parser.add_argument("text", nargs="*", help="Phrase to parse")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run built-in known, unknown, and ambiguous examples",
    )
    args = parser.parse_args()

    if args.demo:
        for phrase in DEMO_PHRASES:
            show_result(phrase)
        return

    if args.text:
        show_result(" ".join(args.text))
        return

    print("Type phrases to test. Enter 'quit' to finish. No actions will move Buck.")
    while True:
        try:
            text = input("command> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if text.lower() in {"quit", "exit"}:
            return
        show_result(text)


if __name__ == "__main__":
    main()
