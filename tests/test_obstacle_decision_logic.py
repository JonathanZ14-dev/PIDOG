"""Check mode isolation and safe handling of missing observations."""

import unittest

from vision_vs_ultrasonic_project1.decision_logic import decide


class DecisionLogicTests(unittest.TestCase):
    def test_vision_ignores_sonar(self):
        self.assertEqual(decide("vision", False, -1, 25)[0], "forward")

    def test_sonar_ignores_vision(self):
        self.assertEqual(decide("ultrasonic", True, 40, 25)[0], "forward")

    def test_combined_stops_for_either_hazard(self):
        self.assertEqual(decide("combined", True, 40, 25)[0], "stop")
        self.assertEqual(decide("combined", False, 20, 25)[0], "stop")

    def test_required_missing_or_invalid_data_stops(self):
        self.assertEqual(decide("vision", None, None, 25)[0], "stop")
        self.assertEqual(decide("ultrasonic", None, -1, 25)[0], "stop")
        self.assertEqual(decide("combined", False, None, 25)[0], "stop")

    def test_sonar_threshold_boundary_stops(self):
        self.assertEqual(decide("ultrasonic", None, 25, 25)[0], "stop")


if __name__ == "__main__":
    unittest.main()
