import unittest
from unittest.mock import MagicMock, patch
from music_player.player_metrics import show_liked_songs
from music_player.player_state import PlayerState


class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.liked_tracks = set()
        self.mock_state.library_tracks = []

    @patch('builtins.print')
    def test_pc1_state_none(self, mock_print):
        show_liked_songs(None)
        mock_print.assert_any_call("[metrics] Error: State is missing.")

    @patch('builtins.print')
    def test_pc3_likes_empty(self, mock_print):
        self.mock_state.liked_tracks = set()
        show_liked_songs(self.mock_state)
        mock_print.assert_any_call("  (No liked songs yet)")

    @patch('builtins.print')
    def test_pc5_lib_corrupt(self, mock_print):
        self.mock_state.liked_tracks = {"song1"}
        self.mock_state.library_tracks = "NotAList"
        show_liked_songs(self.mock_state)
        mock_print.assert_any_call("[metrics] Error: Library data corrupted.")

    @patch('builtins.print')
    def test_pc6_no_match(self, mock_print):
        self.mock_state.liked_tracks = {"/path/songA.mp3"}
        track = MagicMock()
        track.path = "/path/songB.mp3"
        self.mock_state.library_tracks = [track]
        show_liked_songs(self.mock_state)
        mock_print.assert_any_call("  (Liked songs not found in current library scan)")

    @patch('builtins.print')
    def test_pc7_match_found(self, mock_print):
        path = "/path/songA.mp3"
        self.mock_state.liked_tracks = {path}
        track = MagicMock()
        track.path = path
        track.display_name = "My Hit Song"
        self.mock_state.library_tracks = [track]
        show_liked_songs(self.mock_state)
        mock_print.assert_any_call("  ♥ My Hit Song")


if __name__ == '__main__':
    unittest.main()