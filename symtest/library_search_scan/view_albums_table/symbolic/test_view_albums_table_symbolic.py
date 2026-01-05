import unittest
from unittest.mock import MagicMock, patch
from music_player.player_state import PlayerState
from music_player.library_search_scan import view_albums_table

class TestSymbolicExecution(unittest.TestCase):

    @patch('music_player.library_search_scan.print')
    def test_pc1_state_none(self, mock_print):
        state = None
        view_albums_table(state)
        mock_print.assert_not_called()

    @patch('music_player.library_search_scan.print')
    def test_pc1_library_empty(self, mock_print):
        mock_audio_engine = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        view_albums_table(state)
        mock_print.assert_not_called()

    @patch('music_player.library_search_scan.print')
    def test_pc2_execution_logic(self, mock_print):
        mock_audio_engine = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        mock_path = MagicMock()
        mock_path.parent.name = "RockAlbum"
        track1 = MagicMock()
        track1.path = mock_path
        track1.duration_seconds = 125
        state.library_tracks = [track1]
        view_albums_table(state)

        output = str(mock_print.call_args_list)
        self.assertIn("RockAlbum", output)
        self.assertIn("2:05", output)

    @patch('music_player.library_search_scan.print')
    def test_pc2_boundary_duration(self, mock_print):
        mock_audio_engine = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        mock_path = MagicMock()
        mock_path.parent.name = "Unknown"
        track_none_duration = MagicMock()
        track_none_duration.path = mock_path
        track_none_duration.duration_seconds = None
        state.library_tracks = [track_none_duration]
        view_albums_table(state)

        output = str(mock_print.call_args_list)
        self.assertIn("0:00", output)


if __name__ == '__main__':
    unittest.main()