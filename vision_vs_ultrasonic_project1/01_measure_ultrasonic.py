#!/usr/bin/env python3
"""Measure Buck's ultrasonic sensor repeatedly without initializing PiDog motion."""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target-cm",
        type=float,
        required=True,
        help="measured gap from the transducer faces to a flat target, in cm",
    )
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--interval", type=float, default=0.25, help="seconds between readings")
    parser.add_argument("--output", type=Path, help="optional CSV path on Buck")
    args = parser.parse_args()
    if not math.isfinite(args.target_cm) or args.target_cm <= 0:
        parser.error("--target-cm must be a positive, finite number")
    if args.count <= 0:
        parser.error("--count must be positive")
    if not math.isfinite(args.interval) or args.interval < 0:
        parser.error("--interval must be a nonnegative, finite number")
    return args


def main() -> int:
    args = parse_args()

    # Import hardware only after validating arguments. --help works on the Mac.
    from robot_hat import Pin, Ultrasonic

    sensor = Ultrasonic(Pin("D1"), Pin("D0"))
    rows: list[dict[str, object]] = []
    valid_readings: list[float] = []

    print(f"Target: {args.target_cm:g} cm | samples: {args.count}")
    for sample in range(1, args.count + 1):
        timestamp = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
        reading = float(sensor.read())
        valid = math.isfinite(reading) and reading > 0
        if valid:
            valid_readings.append(reading)
        rows.append(
            {
                "sample": sample,
                "timestamp_utc": timestamp,
                "target_cm": args.target_cm,
                "reading_cm": reading,
                "valid": valid,
            }
        )
        status = "valid" if valid else "invalid"
        print(f"{sample:02d}: {reading:7.2f} cm  {status}")
        if sample < args.count:
            time.sleep(args.interval)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=("sample", "timestamp_utc", "target_cm", "reading_cm", "valid"),
            )
            writer.writeheader()
            writer.writerows(rows)
        print(f"CSV saved on Buck: {args.output}")

    print(f"Valid: {len(valid_readings)}/{args.count}")
    if valid_readings:
        median = statistics.median(valid_readings)
        print(f"Median of valid readings: {median:.2f} cm")
        print(f"Median minus measured target: {median - args.target_cm:+.2f} cm")
    else:
        print("No valid readings; check the target and sensor connection.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
