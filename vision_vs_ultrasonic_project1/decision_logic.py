"""Small, print-only decision rule for learning sensor mode isolation."""

from __future__ import annotations

import math
from typing import Optional


def decide(
    mode: str,
    vision_blocked: Optional[bool],
    sonar_cm: Optional[float],
    demo_threshold_cm: float,
) -> tuple[str, str]:
    """Return an illustrative action and reason; this does not move Buck."""
    if mode not in ("vision", "ultrasonic", "combined"):
        raise ValueError(f"unknown mode: {mode}")
    if not math.isfinite(demo_threshold_cm) or demo_threshold_cm <= 0:
        raise ValueError("demo threshold must be positive and finite")

    use_vision = mode in ("vision", "combined")
    use_sonar = mode in ("ultrasonic", "combined")

    if use_vision and vision_blocked is None:
        return "stop", "required vision observation is unknown"
    if use_sonar and (sonar_cm is None or not math.isfinite(sonar_cm) or sonar_cm <= 0):
        return "stop", "required sonar reading is invalid or missing"
    if use_vision and vision_blocked:
        return "stop", "vision reports an obstacle"
    if use_sonar and sonar_cm is not None and sonar_cm <= demo_threshold_cm:
        return "stop", "sonar reports a nearby obstacle"
    return "forward", "selected sensor evidence appears clear"
