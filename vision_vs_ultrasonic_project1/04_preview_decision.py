#!/usr/bin/env python3
"""Preview sensor-mode decisions from supplied observations; never move Buck."""

from __future__ import annotations

import argparse

from decision_logic import decide


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("vision", "ultrasonic", "combined"), required=True)
    parser.add_argument("--vision", choices=("clear", "blocked", "unknown"), default="unknown")
    parser.add_argument("--sonar-cm", type=float, help="example ultrasonic reading in cm")
    parser.add_argument(
        "--demo-threshold-cm",
        type=float,
        default=25,
        help="illustrative stop threshold; not calibrated for robot movement",
    )
    args = parser.parse_args()

    vision_observation = {
        "clear": False,
        "blocked": True,
        "unknown": None,
    }[args.vision]
    try:
        action, reason = decide(
            args.mode, vision_observation, args.sonar_cm, args.demo_threshold_cm
        )
    except ValueError as exc:
        parser.error(str(exc))

    print(f"Mode: {args.mode}")
    print(f"Decision: {action} — {reason}")
    print("Preview only: no sensor was read and no motion command was sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
