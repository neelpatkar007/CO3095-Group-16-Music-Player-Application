import unittest
from unittest.mock import MagicMock, patch
from music_player.player_metrics import toggle_like
from music_player.player_state import PlayerState


class TestConcolicExecution(unittest.TestCase):


    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.current_track = MagicMock()
        self.mock_state.current_track.path = "/music/test.mp3"
        self.mock_state.current_track.display_name = "Test Track"

    @patch('builtins.print')
    def test_iter5_unlike_fail(self, mock_print):
        path = "/music/test.mp3"
        fake_set = MagicMock(spec=set)
        fake_set.__contains__.side_effect = lambda x: True
        fake_set.remove.return_value = None
        self.mock_state.liked_tracks = fake_set

        toggle_like(self.mock_state)
        fake_set.remove.assert_called_with(path)
        mock_print.assert_called_with("[metrics] Error: Failed to remove like.")

    @patch('builtins.print')
    def test_iter7_like_fail(self, mock_print):
        path = "/music/test.mp3"
        fake_set = MagicMock(spec=set)
        fake_set.__contains__.side_effect = [False, False]
        fake_set.add.return_value = None
        self.mock_state.liked_tracks = fake_set
        toggle_like(self.mock_state)
        fake_set.add.assert_called_with(path)
        mock_print.assert_called_with("[metrics] Error: Failed to add like.")


if __name__ == '__main__':
    unittest.main()