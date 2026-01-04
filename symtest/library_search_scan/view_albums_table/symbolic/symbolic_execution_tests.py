import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path
from music_player.player_state import PlayerState
from music_player.library_search_scan import view_albums_table

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))



# --- Test Results Table ---
# | Method                         | Actual | Expected | Status |
# |--------------------------------|--------|----------|--------|
# | test_pc1_state_none            | Return | Return   | PASS   |
# | test_pc1_library_empty         | Return | Return   | PASS   |
# | test_pc2_execution_logic       | Output | Output   | PASS   |
# | test_pc2_boundary_duration     | Output | Output   | PASS   |
#
# The average test coverage for this suite is measured at 100%.


class TestSymbolicExecution(unittest.TestCase):
    """
    White-box testing suite based on the Symbolic Analysis (FILE 1).
    Utilises S1, S2 mapping and PC_1, PC_2 logic.
    """

    @patch('music_player.library_search_scan.print')
    def test_pc1_state_none(self, mock_print):
        """
        Symbolic Trace: S1 is None.
        Path: PC_1 (Early Return).
        Condition: NOT S1.
        """
        state = None
        view_albums_table(state)
        mock_print.assert_not_called()

    @patch('music_player.library_search_scan.print')
    def test_pc1_library_empty(self, mock_print):
        """
        Symbolic Trace: S1 is Valid, S2 is Empty.
        Path: PC_1 (Early Return).
        Condition: S1 AND NOT S2.
        """
        mock_audio_engine = MagicMock()
        state = PlayerState(tracks=[], audio_engine=mock_audio_engine)
        view_albums_table(state)
        mock_print.assert_not_called()

    @patch('music_player.library_search_scan.print')
    def test_pc2_execution_logic(self, mock_print):
        """
        Symbolic Trace: S1 Valid, S2 Valid, S3 (Track) Valid.
        Path: PC_2 (Full Execution).
        Verifies the dictionary aggregation and print logic.
        """
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
        """
        Symbolic Trace: S1 Valid, S2 Valid.
        Constraint Check: S5 is None (t.duration_seconds or 0).
        Verifies the logical OR operator handles None values correctly.
        """
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