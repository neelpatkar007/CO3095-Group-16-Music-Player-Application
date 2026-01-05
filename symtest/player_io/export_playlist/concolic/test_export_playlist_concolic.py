import unittest
from unittest.mock import MagicMock, patch
from music_player.player_io import export_playlist
from music_player.player_state import PlayerState


class TestConcolicExport(unittest.TestCase):

    def test_iteration_1_pc2(self):
        state = MagicMock(spec=PlayerState)
        state.playlists = []
        state.tracks = []
        with patch('builtins.print') as mock_print:
            export_playlist(state, "S2_val", "")
            mock_print.assert_any_call("[export] Nothing to export.")

    @patch("builtins.open", create=True)
    def test_iteration_2_pc3(self, mock_file):
        track = MagicMock()
        track.duration_seconds = 100
        track.display_name = "Test Track"
        track.path = MagicMock()
        track.path.resolve.return_value = "/path/to/track.mp3"

        state = MagicMock(spec=PlayerState)
        state.playlists = []
        state.tracks = [track]

        export_playlist(state, "library", "")
        self.assertTrue(mock_file.called)

    @patch("builtins.open", side_effect=OSError)
    def test_iteration_4_pc4(self, mock_file):
        track = MagicMock()
        track.duration_seconds = 100
        track.display_name = "Test Track"
        track.path = MagicMock()

        state = MagicMock(spec=PlayerState)
        state.playlists = []
        state.tracks = [track]

        with patch('builtins.print') as mock_print:
            export_playlist(state, "invalid/path", "")
            mock_print.assert_any_call("[export] Error writing file (OS): Check permissions or path.")


if __name__ == '__main__':
    unittest.main()