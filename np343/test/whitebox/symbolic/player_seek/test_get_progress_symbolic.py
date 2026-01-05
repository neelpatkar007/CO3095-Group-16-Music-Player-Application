import unittest
from unittest.mock import Mock
from music_player.player_seek import get_progress, Track


class TestSymbolicExecution(unittest.TestCase):

    def test_PC_1(self):
        S1 = None
        result = get_progress(S1)
        self.assertEqual(result, (0.0, None))

    def test_PC_2(self):
        S2 = "NotATrackObject"
        S3 = 10.0
        S1 = Mock()
        S1.current_track = S2
        S1.position_seconds = S3

        result = get_progress(S1)
        self.assertEqual(result, (10.0, None))

    def test_PC_3(self):

        S2 = "NotATrackObject"
        S3 = "InvalidPosition"
        S1 = Mock()
        S1.current_track = S2
        S1.position_seconds = S3

        result = get_progress(S1)
        self.assertEqual(result, (0.0, None))

    def test_PC_4(self):
        S2 = Track("Test Track", 120.0)
        S3 = 50.0
        S1 = Mock()
        S1.current_track = S2
        S1.position_seconds = S3

        result = get_progress(S1)
        self.assertEqual(result, (50.0, None))


if __name__ == '__main__':
    unittest.main()