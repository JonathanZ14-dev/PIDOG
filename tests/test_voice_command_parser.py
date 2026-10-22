import unittest

from src.voice_control.command_parser import (
    has_wake_prefix,
    normalize,
    parse_active_command,
    parse_command,
)


class NormalizeTests(unittest.TestCase):
    def test_normalizes_case_punctuation_and_spaces(self):
        self.assertEqual(normalize("  Hello,   BUCK! "), "hello buck")


class ParseCommandTests(unittest.TestCase):
    def test_known_aliases(self):
        cases = {
            "sit": "sit",
            "sit down": "sit",
            "stand up": "stand",
            "lie down": "lie",
            "wag your tail": "wag_tail",
        }
        for phrase, expected in cases.items():
            with self.subTest(phrase=phrase):
                self.assertEqual(parse_command(phrase).action, expected)

    def test_wake_phrase_and_politeness_are_optional(self):
        result = parse_command("Hello Buck, please sit down!")
        self.assertEqual(result.action, "sit")

    def test_unknown_phrase_produces_no_action(self):
        result = parse_command("run into the kitchen")
        self.assertIsNone(result.action)

    def test_multiple_commands_produce_no_action(self):
        result = parse_command("sit and then stand")
        self.assertIsNone(result.action)

    def test_stop_token_overrides_other_words(self):
        result = parse_command("Buck stop moving right now")
        self.assertEqual(result.action, "stop")

    def test_stop_is_not_a_substring_match(self):
        result = parse_command("Buck is unstoppable")
        self.assertIsNone(result.action)


class ActiveCommandTests(unittest.TestCase):
    def test_wake_prefix_ignores_case_and_punctuation(self):
        self.assertTrue(has_wake_prefix("Hey, BUCK! Sit down."))

    def test_similar_word_is_not_a_wake_prefix(self):
        self.assertFalse(has_wake_prefix("Buckwheat sit down"))

    def test_active_command_accepts_bare_command(self):
        result = parse_active_command("sit down")
        self.assertEqual(result.action, "sit")

    def test_active_command_accepts_wake_prefix(self):
        result = parse_active_command("Hey Buck, please sit down")
        self.assertEqual(result.action, "sit")

    def test_active_stop_does_not_require_wake_prefix(self):
        result = parse_active_command("stop")
        self.assertEqual(result.action, "stop")


if __name__ == "__main__":
    unittest.main()
