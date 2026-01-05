import unittest
from unittest.mock import MagicMock, patch
from music_player.player_state import PlayerState
from music_player.library_search_scan import search_library

class TestSymbolicExecution(unittest.TestCase):

    @patch('music_player.library_search_scan.print')
    def test_pc1_state_none(self, mock_print):
        S1 = None
        S2 = "test"
        search_library(S1, S2)
        mock_print.assert_not_called()

    @patch('music_player.library_search_scan.print')
    def test_pc2_query_empty(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        S2 = ""
        search_library(S1, S2)
        mock_print.assert_called_with("[search] Usage: /search <query>")

    @patch('music_player.library_search_scan.print')
    def test_pc3_library_missing(self, mock_print):
        S1 = MagicMock(spec=[])
        S2 = "test"
        search_library(S1, S2)
        mock_print.assert_called_with("[search] Error: Library unavailable.")

    @patch('music_player.library_search_scan.print')
    def test_pc4_library_corrupted(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        S1.library_tracks = 12345
        S2 = "test"
        search_library(S1, S2)
        mock_print.assert_called_with("[search] Error: Library corrupted.")

    @patch('music_player.library_search_scan.print')
    def test_pc5_empty_list(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        S2 = "test"
        search_library(S1, S2)
        mock_print.assert_called_with("[search] No matches found.")

    @patch('music_player.library_search_scan.print')
    def test_pc6_track_none(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        S1.library_tracks = [None]
        S2 = "test"
        search_library(S1, S2)
        mock_print.assert_called_with("[search] No matches found.")

    @patch('music_player.library_search_scan.print')
    def test_pc7_match_title(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)

        S4 = MagicMock()
        S4.title = "Test Song"
        S4.artist = "Unknown"
        S4.path = None
        S4.duration_seconds = 180

        S1.library_tracks = [S4]
        S2 = "test"
        search_library(S1, S2)
        first_call = mock_print.call_args_list[0][0][0]
        self.assertTrue(first_call.startswith("[search] Found 1 matches"))

    @patch('music_player.library_search_scan.print')
    def test_pc8_match_artist(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)

        S4 = MagicMock()
        S4.title = "Song"
        S4.artist = "Test Artist"
        S4.path = None
        S4.duration_seconds = 180

        S1.library_tracks = [S4]
        S2 = "test"
        search_library(S1, S2)
        first_call = mock_print.call_args_list[0][0][0]
        self.assertTrue(first_call.startswith("[search] Found 1 matches"))

    @patch('music_player.library_search_scan.print')
    def test_pc9_match_path(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)

        mock_path = MagicMock()
        mock_path.name = "test_file.mp3"

        S4 = MagicMock()
        S4.title = "Song"
        S4.artist = "Artist"
        S4.path = mock_path
        S4.duration_seconds = 180

        S1.library_tracks = [S4]
        S2 = "test"
        search_library(S1, S2)
        first_call = mock_print.call_args_list[0][0][0]
        self.assertTrue(first_call.startswith("[search] Found 1 matches"))

    @patch('music_player.library_search_scan.print')
    def test_pc10_no_match_valid_item(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)

        S4 = MagicMock()
        S4.title = "Song"
        S4.artist = "Artist"
        S4.path = None
        S4.duration_seconds = 180

        S1.library_tracks = [S4]
        S2 = "nomatch"
        search_library(S1, S2)
        mock_print.assert_called_with("[search] No matches found.")


if __name__ == '__main__':
    unittest.main()