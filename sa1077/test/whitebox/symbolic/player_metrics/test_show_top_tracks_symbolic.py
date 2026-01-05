import unittest
from unittest.mock import MagicMock, patch
from music_player.player_metrics import show_top_tracks
from music_player.player_state import PlayerState


class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.play_counts = {}
        self.mock_state.library_tracks = []

    @patch('builtins.print')
    def test_pc1_state_none(self, mock_print):
        show_top_tracks(None)
        mock_print.assert_any_call("[metrics] Error: State is None.")

    @patch('builtins.print')
    def test_pc3_corrupt_type(self, mock_print):
        self.mock_state.play_counts = "NotADict"
        show_top_tracks(self.mock_state)
        mock_print.assert_any_call("[metrics] Error: Play counts corrupted.")

    @patch('builtins.print')
    def test_pc4_empty_data(self, mock_print):
        self.mock_state.play_counts = {}
        show_top_tracks(self.mock_state)
        mock_print.assert_any_call("[metrics] No play history yet.")

    @patch('builtins.sorted')
    @patch('builtins.print')
    def test_pc5_sort_fail(self, mock_print, mock_sorted):
        self.mock_state.play_counts = {"song1": 5}
        mock_sorted.side_effect = ValueError("Sort Comparison Error")

        show_top_tracks(self.mock_state)
        mock_print.assert_any_call("[metrics] Error sorting play history.")

    @patch('builtins.print')
    def test_pc8_valid_display(self, mock_print):
        path = "/music/hit.mp3"
        self.mock_state.play_counts = {path: 100}
        track = MagicMock()
        track.path = path
        track.display_name = "Greatest Hit"
        self.mock_state.library_tracks = [track]
        show_top_tracks(self.mock_state)
        mock_print.assert_any_call("[metrics] --- Top Played Songs ---")
        mock_print.assert_any_call("  100 plays: Greatest Hit")


if __name__ == '__main__':
    unittest.main()