import unittest
from unittest.mock import Mock, patch
from music_player.player_seek import nudge


class TestSymbolicNudge(unittest.TestCase):

    @patch('music_player.player_seek.seek_to')
    def test_pc1(self, mock_seek):
        s1 = None
        s2 = 0.0
        s3 = 5.0

        nudge(s1, s3)
        mock_seek.assert_not_called()

    @patch('music_player.player_seek.seek_to')
    def test_pc2(self, mock_seek):
        s1 = Mock()
        s1.position_seconds = "invalid_type"  # S2
        s3 = 5.0

        nudge(s1, s3)
        mock_seek.assert_called_once_with(s1, 5.0)

    @patch('music_player.player_seek.seek_to')
    def test_pc3(self, mock_seek):
        """Path PC_3: S1 is Object, S2 is valid float"""
        s1 = Mock()
        s1.position_seconds = 10.0
        s3 = 5.0

        nudge(s1, s3)
        mock_seek.assert_called_once_with(s1, 15.0)


if __name__ == '__main__':
    unittest.main()