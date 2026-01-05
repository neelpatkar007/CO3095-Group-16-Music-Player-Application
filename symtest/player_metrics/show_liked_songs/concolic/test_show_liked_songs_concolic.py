import unittest
from unittest.mock import MagicMock, patch
from music_player.player_metrics import show_liked_songs
from music_player.player_state import PlayerState


class TestConcolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.liked_tracks = {"/music/fav.mp3"}

    @patch('builtins.print')
    def test_iter_invalid_items(self, mock_print):
        t1 = None
        t2 = MagicMock()
        del t2.path
        self.mock_state.library_tracks = [t1, t2]
        show_liked_songs(self.mock_state)
        mock_print.assert_any_call("  (Liked songs not found in current library scan)")

    @patch('builtins.print')
    def test_iter_derive_match(self, mock_print):
        t1 = MagicMock()
        t1.path = "/music/fav.mp3"
        t1.display_name = "Concolic Symphony"
        self.mock_state.library_tracks = [t1]
        show_liked_songs(self.mock_state)
        mock_print.assert_any_call("  ♥ Concolic Symphony")

    @patch('builtins.print')
    def test_iter_unknown_name(self, mock_print):
        t1 = MagicMock()
        t1.path = "/music/fav.mp3"
        t1.display_name = None
        self.mock_state.library_tracks = [t1]
        show_liked_songs(self.mock_state)
        mock_print.assert_any_call("  ♥ Unknown Title")


if __name__ == '__main__':
    unittest.main()