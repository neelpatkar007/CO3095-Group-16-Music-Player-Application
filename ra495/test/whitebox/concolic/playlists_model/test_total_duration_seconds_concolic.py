import unittest
from unittest.mock import MagicMock



class TestConcolicTesting(unittest.TestCase):


    def test_iteration_1_base(self):
        mock_obj = MagicMock()
        mock_obj.tracks = []

        total = 0.0
        for t in mock_obj.tracks:
            dur = getattr(t, "duration_seconds", None)
            if isinstance(dur, (int, float)) and dur > 0:
                total += float(dur)
        self.assertEqual(total, 0.0)

    def test_iteration_2_flip_type(self):
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