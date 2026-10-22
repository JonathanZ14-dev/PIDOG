"""Convert recognized speech into a deliberately small action allowlist."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Literal


Action = Literal["sit", "stand", "lie", "wag_tail", "stop"]


ALIASES: dict[str, Action] = {
    "sit": "sit",
    "sit down": "sit",
    "stand": "stand",
    "stand up": "stand",
    "lie": "lie",
    "lie down": "lie",
    "lay down": "lie",
    "wag tail": "wag_tail",
    "wag your tail": "wag_tail",
    "stop": "stop",
}

WAKE_PREFIXES = ("hey buck", "hello buck", "buck")


@dataclass(frozen=True)
class ParseResult:
    original_text: str
    normalized_text: str
    action: Action | None
    reason: str

    @property
    def recognized(self) -> bool:
        return self.action is not None


def normalize(text: str) -> str:
    """Lowercase text, remove punctuation, and collapse repeated whitespace."""
    words_only = re.sub(r"[^a-z0-9']+", " ", text.lower())
    return " ".join(words_only.split())


def _remove_optional_words(text: str) -> str:
    """Remove an optional wake phrase and polite wrapper."""
    for prefix in WAKE_PREFIXES:
        if text == prefix:
            return ""
        if text.startswith(prefix + " "):
            text = text[len(prefix) + 1 :]
            break

    if text.startswith("please "):
        text = text[len("please ") :]
    if text.endswith(" please"):
        text = text[: -len(" please")]
    return text.strip()


def has_wake_prefix(text: str) -> bool:
    """Return whether normalized text starts with one complete wake phrase."""
    normalized = normalize(text)
    return any(
        normalized == prefix or normalized.startswith(prefix + " ")
        for prefix in WAKE_PREFIXES
    )


def parse_command(text: str) -> ParseResult:
    """Return one approved action, or no action when the phrase is unknown."""
    normalized = normalize(text)

    # An isolated `stop` token always wins. A false stop is safer than allowing
    # another movement command to proceed.
    if "stop" in normalized.split():
        return ParseResult(text, normalized, "stop", "emergency stop token")

    command_text = _remove_optional_words(normalized)
    action = ALIASES.get(command_text)
    if action is None:
        return ParseResult(text, normalized, None, "not in the action allowlist")
    return ParseResult(text, normalized, action, f"matched {command_text!r}")


def parse_active_command(text: str) -> ParseResult:
    """Parse one command heard by the continuously listening loop."""
    return parse_command(text)
