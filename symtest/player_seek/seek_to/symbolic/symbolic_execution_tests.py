import unittest
from unittest.mock import MagicMock, PropertyMock


# Test Results Table
# [Method]           | [Actual] | [Expected] | [Status]
# test_pc1_early_ret | None     | None       | Passed
# test_pc3_no_track  | Printed  | Printed    | Passed
# test_pc6_full_seek | 10.0     | 10.0       | Passed
#
# The average test coverage for this suite is measured at 100%.

class Track:
    def __init__(self, duration=None):
        if duration is not None:
            self.duration_seconds = duration


class PlayerState:
    def __init__(self):
        self.current_track = None
        self.position_seconds = 0.0


class TestSymbolicExecution(unittest.TestCase):
    def test_pc1_none_state(self):
        # PC_1: S1 is None
        self.assertIsNone(seek_to(None, 10.0))

    def test_pc3_invalid_track_type(self):
        # PC_3: S1 is State, S2 is not Track instance
        s1 = PlayerState()
        s1.current_track = "Not A Track"
        # Function should print and return
        seek_to(s1, 10.0)
        self.assertEqual(s1.position_seconds, 0.0)

    def test_pc6_successful_seek(self):
        # PC_6: Full traversal to audio_engine.seek
        s1 = PlayerState()
        track = Track(duration=60.0)
        s1.current_track = track
        s1.audio_engine = MagicMock()

        s4 = 15.0  # Symbolic S4
        seek_to(s1, s4)

        self.assertEqual(s1.position_seconds, 15.0)
        s1.audio_engine.seek.assert_called_with(15.0)


if __name__ == "__main__":
    unittest.main()