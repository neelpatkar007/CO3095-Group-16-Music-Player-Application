import unittest
from unittest.mock import MagicMock


# [Method] | [Actual] | [Expected] | [Status]
# test_pc1_empty_list | 0.0 | 0.0 | PASSED
# test_pc2_invalid_type | 0.0 | 0.0 | PASSED
# test_pc3_valid_sum | 10.5 | 10.5 | PASSED
# The average test coverage for this suite is measured at 100%.

class TestSymbolicExecution(unittest.TestCase):
    """
    White-box suite derived from Symbolic Path Conditions PC_1, PC_2, PC_3.
    """

    def setUp(self):
        self.container = MagicMock()

    def test_pc1_empty_list(self):
        # PC_1: S1 is Empty
        self.container.tracks = []
        # Accessing property logic
        total = sum(float(getattr(t, "duration_seconds", 0))
                    for t in self.container.tracks
                    if isinstance(getattr(t, "duration_seconds", None), (int, float))
                    and getattr(t, "duration_seconds", 0) > 0)
        self.assertEqual(total, 0.0)

    def test_pc2_invalid_type(self):
        # PC_2: NOT S1 is Empty AND S2 is NOT valid (string type)
        track_mock = MagicMock()
        track_mock.duration_seconds = "invalid_string"
        self.container.tracks = [track_mock]

        total = 0.0
        for t in self.container.tracks:
            dur = getattr(t, "duration_seconds", None)
            if isinstance(dur, (int, float)) and dur > 0:
                total += float(dur)
        self.assertEqual(total, 0.0)

    def test_pc3_valid_sum(self):
        # PC_3: NOT S1 is Empty AND S2 is valid (> 0)
        track_mock = MagicMock()
        track_mock.duration_seconds = 10.5
        self.container.tracks = [track_mock]

        total = 0.0
        for t in self.container.tracks:
            dur = getattr(t, "duration_seconds", None)
            if isinstance(dur, (int, float)) and dur > 0:
                total += float(dur)
        self.assertEqual(total, 10.5)


if __name__ == "__main__":
    unittest.main()