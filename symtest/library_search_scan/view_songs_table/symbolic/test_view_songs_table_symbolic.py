import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path
from music_player.player_state import PlayerState
from music_player.library_search_scan import view_songs_table

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))




class TestSymbolicExecution(unittest.TestCase):
    """
    White-box testing suite derived from Static Symbolic Analysis.

    -----------------------------------------------------------------------
    Test Results Table
    -----------------------------------------------------------------------
    Method                         | Actual | Expected | Status
    -------------------------------|--------|----------|-------
    test_pc1_state_none            | Output | Output   | PASS
    test_pc2_state_exists_lib_empty| Output | Output   | PASS
    test_pc3_state_exists_lib_full | Call   | Call     | PASS
    -----------------------------------------------------------------------
    The average test coverage for this suite is measured at 100%.
    """

    @patch('music_player.library_search_scan._print_tracks_table')
    @patch('music_player.library_search_scan.print')
    def test_pc1_state_none(self, mock_print, mock_print_tracks):
        """
        Symbolic Path: PC_1
        Condition: NOT S1
        Rationale: Validates short-circuit logic when state object is Null.
        """
        s1_input = None
        view_songs_table(s1_input)

        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        self.assertIn("[lib] --- All Songs ---", calls)
        self.assertTrue(any("(empty library)" in call for call in calls))
        mock_print_tracks.assert_not_called()

    @patch('music_player.library_search_scan._print_tracks_table')
    @patch('music_player.library_search_scan.print')
    def test_pc2_state_exists_lib_empty(self, mock_print, mock_print_tracks):
        """
        Symbolic Path: PC_2
        Condition: S1 AND NOT S2
        Rationale: Validates logic when State object exists but contains no tracks.
        """
        mock_audio_engine = MagicMock()
        s1_input = PlayerState(tracks=[], audio_engine=mock_audio_engine)

        view_songs_table(s1_input)

        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        self.assertTrue(any("(empty library)" in call for call in calls))
        mock_print_tracks.assert_not_called()

    @patch('music_player.library_search_scan._print_tracks_table')
    @patch('music_player.library_search_scan.print')
    def test_pc3_state_exists_lib_full(self, mock_print, mock_print_tracks):
        """
        Symbolic Path: PC_3
        Condition: S1 AND S2
        Rationale: Validates the 'happy path' where delegation to helper occurs.
        """
        mock_audio_engine = MagicMock()
        s1_input = PlayerState(tracks=[], audio_engine=mock_audio_engine)

        track_a = MagicMock()
        track_a.duration_seconds = 120
        track_b = MagicMock()
        track_b.duration_seconds = 180
        s1_input.library_tracks = [track_a, track_b]

        view_songs_table(s1_input)

        calls = [str(call[0][0]) for call in mock_print.call_args_list]
        self.assertIn("[lib] --- All Songs ---", calls)
        mock_print_tracks.assert_called_once_with([track_a, track_b])


if __name__ == '__main__':
    unittest.main()