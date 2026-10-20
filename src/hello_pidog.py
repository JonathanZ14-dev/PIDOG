#!/usr/bin/env python3
"""A deliberately guarded, low-speed first PiDog movement program."""

from __future__ import annotations

import argparse
import time

from pidog import Pidog


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--i-have-calibrated",
        action="store_true",
        help="confirm that official servo calibration is complete",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.i_have_calibrated:
        print("Refusing to move: calibrate PiDog first, then use --i-have-calibrated.")
        return 2

    dog = Pidog()
    try:
        time.sleep(0.5)
        print("Moving slowly into a sitting posture...")
        dog.do_action("sit", speed=30)
        dog.wait_all_done()
        print("Sitting complete. Wagging tail four times...")
        dog.do_action("wag_tail", step_count=4, speed=40)
        dog.wait_all_done()
        time.sleep(1)
        print("First calibrated movement test completed.")
        return 0
    finally:
        dog.close()


if __name__ == "__main__":
    raise SystemExit(main())
