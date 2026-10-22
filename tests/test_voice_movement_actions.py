import unittest

from src.voice_control.command_parser import ALIASES
from src.voice_control.movement_actions import (
    MOTION_ACTIONS,
    perform_approved_action,
)


class FakeDog:
    def __init__(self):
        self.calls = []

    def do_action(self, name, **kwargs):
        self.calls.append(("do_action", name, kwargs))

    def wait_all_done(self):
        self.calls.append(("wait_all_done",))


class MovementActionTests(unittest.TestCase):
    def test_every_parser_action_is_handled_or_stop(self):
        self.assertEqual(set(ALIASES.values()), MOTION_ACTIONS | {"stop"})

    def test_posture_action_uses_bounded_speed_and_waits(self):
        dog = FakeDog()
        perform_approved_action(dog, "sit")
        self.assertEqual(
            dog.calls,
            [("do_action", "sit", {"speed": 40}), ("wait_all_done",)],
        )

    def test_tail_action_has_bounded_repetitions(self):
        dog = FakeDog()
        perform_approved_action(dog, "wag_tail")
        self.assertEqual(
            dog.calls,
            [
                ("do_action", "wag_tail", {"step_count": 4, "speed": 40}),
                ("wait_all_done",),
            ],
        )

    def test_unapproved_action_is_rejected(self):
        dog = FakeDog()
        with self.assertRaises(ValueError):
            perform_approved_action(dog, "forward")
        self.assertEqual(dog.calls, [])


if __name__ == "__main__":
    unittest.main()
