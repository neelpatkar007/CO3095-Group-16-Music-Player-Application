import unittest
from unittest.mock import MagicMock
from music_player.player_queue import _find_track


class TestConcolicExecution(unittest.TestCase):

    def test_iteration_1_base_case(self):
        s1 = MagicMock(spec=[])
        s2 = "abc"

        result = _find_track(s1, s2)
        self.assertIsNone(result)

    def test_iteration_3_numeric_bounds(self):
        mock_track = MagicMock()
        s1 = MagicMock()
        s1.library_tracks = [mock_track]
        s2 = "1"

        result = _find_track(s1, s2)
        self.assertEqual(result, mock_track)

    def test_iteration_4_name_match(self):
        mock_track = MagicMock()
        mock_track.display_name = "abc song"

        s1 = MagicMock()
        s1.library_tracks = [mock_track]
        s2 = "abc"

        result = _find_track(s1, s2)
        self.assertEqual(result, mock_track)

    def test_iteration_5_forced_exception(self):
        s1 = None
        s2 = None

        result = _find_track(s1, s2)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()