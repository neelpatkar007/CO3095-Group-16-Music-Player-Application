import unittest
from unittest.mock import MagicMock, patch
from music_player.player_state import PlayerState
from music_player.library_search_scan import view_artists_table

class TestSymbolicExecution(unittest.TestCase):

    @patch('music_player.library_search_scan.print')
    def test_pc1_state_none(self, mock_print):
        S1 = None
        view_artists_table(S1)
        mock_print.assert_not_called()

    @patch('music_player.library_search_scan.print')
    def test_pc2_no_library_attrs(self, mock_print):
        S1 = MagicMock(spec=[])
        view_artists_table(S1)
        mock_print.assert_called_with("[lib] Error: Library unavailable.")

    @patch('music_player.library_search_scan.print')
    def test_pc3_empty_library(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        view_artists_table(S1)
        mock_print.assert_called_with("  (no artists found)")

    @patch('music_player.library_search_scan.print')
    def test_pc4_to_pc8_track_logic(self, mock_print):
        mock_audio_engine = MagicMock()
        S1 = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        t1 = None
        t2 = MagicMock(spec=['duration_seconds'])
        t2.duration_seconds = 100
        t3 = MagicMock()
        t3.artist = None
        t3.duration_seconds = 100
        t4 = MagicMock()
        t4.artist = "   "
        t4.duration_seconds = 100
        t5 = MagicMock()
        t5.artist = "Pink Floyd"
        t5.duration_seconds = 300

        S1.library_tracks = [t1, t2, t3, t4, t5]
        view_artists_table(S1)

        output_strings = [str(args[0][0]) for args in mock_print.call_args_list]
        full_output = "\n".join(output_strings)

        self.assertIn("Pink Floyd", full_output)
        self.assertIn("Unknown", full_output)
        self.assertTrue("1" in full_output and "Pink Floyd" in full_output)
        found_unknown = any("Unknown" in line and "3" in line for line in output_strings)
        self.assertTrue(found_unknown, "Failed to aggregate Unknown tracks correctly")


if __name__ == '__main__':
    unittest.main()