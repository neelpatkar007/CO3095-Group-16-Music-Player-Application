import unittest
from unittest.mock import MagicMock


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):

        self.mock_self = MagicMock()

    def _get_target_property(self, instance):


        class TargetClass:
            @property
            def total_duration_seconds(self) -> float:
                total = 0.0
                for t in self.tracks:
                    dur = getattr(t, "duration_seconds", None)
                    if isinstance(dur, (int, float)) and dur > 0:
                        total += float(dur)
                return total

        return TargetClass.total_duration_seconds.fget(instance)

    def test_pc1_empty_list(self):

        self.mock_self.tracks = []

        result = self._get_target_property(self.mock_self)
        self.assertEqual(result, 0.0, "PC_1 failed: Empty list should return 0.0")

    def test_pc2_non_numeric(self):

        mock_track = MagicMock()
        mock_track.duration_seconds = "invalid"
        self.mock_self.tracks = [mock_track]

        result = self._get_target_property(self.mock_self)
        self.assertEqual(result, 0.0, "PC_2 failed: Non-numeric S2 should be ignored")

    def test_pc3_non_positive(self):

        mock_track = MagicMock()
        mock_track.duration_seconds = -5.0
        self.mock_self.tracks = [mock_track]

        result = self._get_target_property(self.mock_self)
        self.assertEqual(result, 0.0, "PC_3 failed: Negative S2 should be ignored")

    def test_pc4_valid_positive(self):

        mock_track = MagicMock()
        mock_track.duration_seconds = 10.5
        self.mock_self.tracks = [mock_track]

        result = self._get_target_property(self.mock_self)
        self.assertEqual(result, 10.5, "PC_4 failed: Positive S2 should be summed")


if __name__ == '__main__':
    unittest.main()