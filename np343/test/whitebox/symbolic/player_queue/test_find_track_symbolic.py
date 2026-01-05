import unittest
from unittest.mock import MagicMock
from music_player.player_queue import _find_track

class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_track_1 = MagicMock()
        self.mock_track_1.display_name = "Symphony No. 5"

        self.mock_track_2 = MagicMock()
        self.mock_track_2.display_name = "Bohemian Rhapsody"

        self.valid_state = MagicMock()
        self.valid_state.library_tracks = [self.mock_track_1, self.mock_track_2]

    def test_pc1_numeric_success(self):
        s1 = self.valid_state
        s2 = "1"

        result = _find_track(s1, s2)

        self.assertEqual(result, self.mock_track_1, "PC_1 failed: Should return track at index 0")

    def test_pc2_string_match_success(self):
        s1 = self.valid_state
        s2 = "Bohemian"

        result = _find_track(s1, s2)

        self.assertEqual(result, self.mock_track_2, "PC_2 failed: Should return track by name match")

    def test_pc3_numeric_fail_string_fail(self):
        s1 = self.valid_state
        s2 = "99"

        result = _find_track(s1, s2)

        self.assertIsNone(result, "PC_3 failed: Should return None for out of bounds index and no name match")

    def test_pc4_exception_handling(self):
        s1 = self.valid_state
        s2 = None

        result = _find_track(s1, s2)

        self.assertIsNone(result, "PC_4 failed: Should return None when exception is caught")


if __name__ == '__main__':
    unittest.main()