import unittest
from unittest.mock import MagicMock, patch
from music_player.player_state import PlayerState
from music_player.library_search_scan import search_library


class TestConcolicExecution(unittest.TestCase):

    @patch('music_player.library_search_scan.print')
    def test_iter_1_base_null(self, mock_print):
        s1_state = None
        s2_query = "rock"
        search_library(s1_state, s2_query)
        mock_print.assert_not_called()

    @patch('music_player.library_search_scan.print')
    def test_iter_2_flip_empty_query(self, mock_print):
        mock_audio_engine = MagicMock()
        s1_state = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        s2_query = ""
        search_library(s1_state, s2_query)
        mock_print.assert_called_with("[search] Usage: /search <query>")

    @patch('music_player.library_search_scan.print')
    def test_iter_3_flip_missing_attr(self, mock_print):
        s1_state = MagicMock(spec=[])
        s2_query = "rock"
        search_library(s1_state, s2_query)
        mock_print.assert_called_with("[search] Error: Library unavailable.")

    @patch('music_player.library_search_scan.print')
    def test_iter_4_flip_corrupt_type(self, mock_print):
        mock_audio_engine = MagicMock()
        s1_state = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        s1_state.library_tracks = 123  # Not a list
        s2_query = "rock"
        search_library(s1_state, s2_query)
        mock_print.assert_called_with("[search] Error: Library corrupted.")

    @patch('music_player.library_search_scan.print')
    def test_iter_5_flip_empty_list(self, mock_print):
        mock_audio_engine = MagicMock()
        s1_state = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        s2_query = "rock"
        search_library(s1_state, s2_query)
        mock_print.assert_called_with("[search] No matches found.")

    @patch('music_player.library_search_scan.print')
    def test_iter_6_flip_match_found(self, mock_print):
        mock_audio_engine = MagicMock()
        s1_state = PlayerState(tracks=[], audio_engine=mock_audio_engine)

        mock_track = MagicMock()
        mock_track.title = "Rock Anthem"
        mock_track.artist = "Band"
        mock_track.path = None
        mock_track.duration_seconds = 180

        s1_state.library_tracks = [mock_track]
        s2_query = "rock"
        search_library(s1_state, s2_query)

        first_call = mock_print.call_args_list[0][0][0]
        self.assertTrue(first_call.startswith("[search] Found 1 matches"))


if __name__ == '__main__':
    unittest.main()