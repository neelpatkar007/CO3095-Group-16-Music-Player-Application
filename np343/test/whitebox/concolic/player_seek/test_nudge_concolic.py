import unittest
from unittest.mock import Mock, patch
from music_player.player_seek import nudge


class TestConcolicNudge(unittest.TestCase):
    @patch('music_player.player_seek.seek_to')
    def test_iteration_1(self, mock_seek):
        s1, s3 = None, 5.0

        nudge(s1, s3)
        mock_seek.assert_not_called()

    @patch('music_player.player_seek.seek_to')
    def test_iteration_2(self, mock_seek):
        s1 = Mock()
        s1.position_seconds = "string"  # S2
        s3 = 5.0

        nudge(s1, s3)
        mock_seek.assert_called_with(s1, 5.0)

    @patch('music_player.player_seek.seek_to')
    def test_iteration_3(self, mock_seek):
        s1 = Mock()
        s1.position_seconds = 10.0  # S2
        s3 = 5.0

        nudge(s1, s3)
        mock_seek.assert_called_with(s1, 15.0)


if __name__ == '__main__':
    unittest.main()