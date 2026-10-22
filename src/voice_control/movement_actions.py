"""The only approved bridge from parsed voice actions to PiDog movement."""

from __future__ import annotations

from typing import Any


MOTION_ACTIONS = frozenset({"sit", "stand", "lie", "wag_tail"})


def perform_approved_action(dog: Any, action: str) -> None:
    """Perform one bounded, low-speed action and wait for it to finish."""
    if action == "sit":
        dog.do_action("sit", speed=40)
    elif action == "stand":
        dog.do_action("stand", speed=50)
    elif action == "lie":
        dog.do_action("lie", speed=40)
    elif action == "wag_tail":
        dog.do_action("wag_tail", step_count=4, speed=40)
    else:
        raise ValueError(f"action is not approved for motion: {action!r}")

    dog.wait_all_done()
