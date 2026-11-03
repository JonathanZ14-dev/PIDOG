#!/usr/bin/env python3
"""Save one camera frame and one ultrasonic reading without moving Buck."""

from __future__ import annotations

import argparse
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="new directory on Buck for the JPEG and JSON record",
    )
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error("--output-dir already exists; choose a new name for each run")

    # These imports open hardware only when the program runs on Buck.
    from picamera2 import Picamera2
    from robot_hat import Pin, Ultrasonic

    args.output_dir.mkdir(parents=True)
    image_path = args.output_dir / "camera.jpg"
    record_path = args.output_dir / "sensor_reading.json"

    camera = Picamera2()
    try:
        camera.configure(camera.create_still_configuration(main={"size": (640, 480)}))
        camera.start()
        time.sleep(1)
        camera.capture_file(str(image_path))
        camera_time = timestamp()
    finally:
        camera.close()

    sensor = Ultrasonic(Pin("D1"), Pin("D0"))
    distance_cm = float(sensor.read())
    sonar_time = timestamp()
    sonar_valid = math.isfinite(distance_cm) and distance_cm > 0

    record = {
        "camera_file": image_path.name,
        "camera_captured_utc": camera_time,
        "sonar_read_utc": sonar_time,
        "sonar_distance_cm": distance_cm if math.isfinite(distance_cm) else None,
        "sonar_valid": sonar_valid,
        "note": "Sequential snapshot; the camera and sonar were not sampled simultaneously.",
    }
    record_path.write_text(json.dumps(record, indent=2) + "\n")

    print(f"Image on Buck: {image_path}")
    print(f"Reading on Buck: {record_path}")
    print(f"Sonar: {distance_cm:g} cm ({'valid' if sonar_valid else 'invalid'})")
    print("No PiDog motion commands were sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
