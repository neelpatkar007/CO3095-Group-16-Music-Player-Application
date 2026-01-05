import unittest
from unittest.mock import MagicMock, patch
from music_player.player_state import PlayerState
from music_player.library_search_scan import view_albums_table

class TestConcolicExecution(unittest.TestCase):

    @patch('music_player.library_search_scan.print')
    def test_iteration_1_base_case(self, mock_print):
        state = None
        view_albums_table(state)
        mock_print.assert_not_called()

    @patch('music_player.library_search_scan.print')
    def test_iteration_2_flip_not_s2(self, mock_print):
        mock_audio_engine = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        view_albums_table(state)
        mock_print.assert_not_called()

    @patch('music_player.library_search_scan.print')
    def test_iteration_3_flip_not_s4(self, mock_print):
        mock_audio_engine = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        mock_path = MagicMock()
        mock_path.parent.name = ""
        track = MagicMock()
        track.path = mock_path
        track.duration_seconds = 60
        state.library_tracks = [track]
        view_albums_table(state)

        output = str(mock_print.call_args_list)
        self.assertIn("(no folder)", output)

    @patch('music_player.library_search_scan.print')
    def test_iteration_4_valid_s4(self, mock_print):
        mock_audio_engine = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        mock_path = MagicMock()
        mock_path.parent.name = "Greatest Hits"
        track = MagicMock()
        track.path = mock_path
        track.duration_seconds = 3600
        state.library_tracks = [track]
        view_albums_table(state)

        output = str(mock_print.call_args_list)
        self.assertIn("Greatest Hits", output)


if __name__ == '__main__':
    unittest.main()