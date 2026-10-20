#!/usr/bin/env python3
"""Verify PiDog's core Python modules without initializing the hardware."""

from __future__ import annotations

import importlib
import platform
from importlib.metadata import PackageNotFoundError, version


def check_module(name: str, distribution: str) -> bool:
    try:
        module = importlib.import_module(name)
    except Exception as exc:  # Show installation errors without hiding the cause.
        print(f"[FAIL] {name}: {exc}")
        return False

    try:
        installed_version = version(distribution)
    except PackageNotFoundError:
        location = getattr(module, "__file__", "unknown location")
        print(
            f"[FAIL] {name}: import found at {location}, but the "
            f"{distribution!r} package is not installed"
        )
        return False

    location = getattr(module, "__file__", "built in")
    print(f"[ OK ] {name}: {installed_version} ({location})")
    return True


def main() -> int:
    print(f"Host: {platform.node()}")
    print(f"Python: {platform.python_version()} ({platform.machine()})")

    required = (
        ("pidog", "pidog"),
        ("robot_hat", "robot-hat"),
        ("vilib", "vilib"),
    )
    results = [check_module(module, distribution) for module, distribution in required]
    required_ok = all(results)

    if required_ok:
        print("PiDog core modules are ready. No servos were moved.")
        return 0

    print("PiDog setup is incomplete. Run scripts/setup_pi.sh on the Pi.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
