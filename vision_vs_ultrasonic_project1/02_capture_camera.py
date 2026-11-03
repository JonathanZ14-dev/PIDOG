#!/usr/bin/env python3
"""Save one camera image on Buck without initializing PiDog motion."""

from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/tmp/pidog-camera-test.jpg"),
        help="JPEG path on Buck",
    )
    args = parser.parse_args()
    if args.output.suffix.lower() not in (".jpg", ".jpeg"):
        parser.error("--output must end in .jpg or .jpeg")

    # Import on Buck, after parsing arguments, so --help also works on the Mac.
    from picamera2 import Picamera2

    camera = Picamera2()
    try:
        camera.configure(camera.create_still_configuration(main={"size": (640, 480)}))
        camera.start()
        time.sleep(1)  # Give automatic exposure and white balance time to settle.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        camera.capture_file(str(args.output))
        captured_at = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    finally:
        camera.close()

    print(f"Captured: {captured_at}")
    print(f"JPEG on Buck: {args.output} ({args.output.stat().st_size} bytes)")
    print("No PiDog motion commands were sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
