import unittest
from unittest.mock import MagicMock


class TestSymbolicExecution(unittest.TestCase):


    def setUp(self):
        self.container = MagicMock()

    def test_pc1_empty_list(self):
        self.container.tracks = []
        total = sum(float(getattr(t, "duration_seconds", 0))
                    for t in self.container.tracks
                    if isinstance(getattr(t, "duration_seconds", None), (int, float))
                    and getattr(t, "duration_seconds", 0) > 0)
        self.assertEqual(total, 0.0)

    def test_pc2_invalid_type(self):
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