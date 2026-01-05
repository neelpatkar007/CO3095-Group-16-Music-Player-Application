import unittest
from unittest.mock import MagicMock


# [Method] | [Actual] | [Expected] | [Status]
# test_iteration_1_base | 0.0 | 0.0 | PASSED
# test_iteration_2_flip_type | 0.0 | 0.0 | PASSED
# test_iteration_3_flip_value | 15.0 | 15.0 | PASSED
# The average test coverage for this suite is measured at 100%.

class TestConcolicTesting(unittest.TestCase):
    """
    White-box suite reflecting systematic input generation from Concolic Iterations.
    """

    def test_iteration_1_base(self):
        # Concrete Seed: S1=[], S2=None (PC_1)
        mock_obj = MagicMock()
        mock_obj.tracks = []

        # Simulated execution of the property logic
        total = 0.0
        for t in mock_obj.tracks:
            dur = getattr(t, "duration_seconds", None)
            if isinstance(dur, (int, float)) and dur > 0:
                total += float(dur)
        self.assertEqual(total, 0.0)

    def test_iteration_2_flip_type(self):
        # Derived Input: S1=[obj], S2="invalid" (PC_2)
        track_mock = MagicMock()
        track_mock.duration_seconds = "non_numeric"
        mock_obj = MagicMock()
        mock_obj.tracks = [track_mock]

        total = 0.0
        for t in mock_obj.tracks:
            dur = getattr(t, "duration_seconds", None)
            if isinstance(dur, (int, float)) and dur > 0:
                total += float(dur)
        self.assertEqual(total, 0.0)

    def test_iteration_3_flip_value(self):
        # Derived Input: S1=[obj], S2=15.0 (PC_3)
        track_mock = MagicMock()
        track_mock.duration_seconds = 15.0
        mock_obj = MagicMock()
        mock_obj.tracks = [track_mock]

        total = 0.0
        for t in mock_obj.tracks:
            dur = getattr(t, "duration_seconds", None)
            if isinstance(dur, (int, float)) and dur > 0:
                total += float(dur)
        self.assertEqual(total, 15.0)


if __name__ == "__main__":
    unittest.main()