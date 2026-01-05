import unittest
from unittest.mock import MagicMock


class TestConcolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_self = MagicMock()

    def _execute_target(self, instance):
        """
        Helper to execute the property logic.
        """

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

    def test_iteration_1_empty(self):
        self.mock_self.tracks = []  # S1

        result = self._execute_target(self.mock_self)
        self.assertEqual(result, 0.0)

    def test_iteration_2_invalid_type(self):
        track = MagicMock()
        track.duration_seconds = "invalid"  # S2
        self.mock_self.tracks = [track]  # S1

        result = self._execute_target(self.mock_self)
        self.assertEqual(result, 0.0)

    def test_iteration_3_boundary_value(self):
        track = MagicMock()
        track.duration_seconds = -5.0  # S2
        self.mock_self.tracks = [track]  # S1

        result = self._execute_target(self.mock_self)
        self.assertEqual(result, 0.0)

    def test_iteration_4_success_path(self):
        track = MagicMock()
        track.duration_seconds = 10.5  # S2
        self.mock_self.tracks = [track]  # S1

        result = self._execute_target(self.mock_self)
        self.assertEqual(result, 10.5)


if __name__ == '__main__':
    unittest.main()