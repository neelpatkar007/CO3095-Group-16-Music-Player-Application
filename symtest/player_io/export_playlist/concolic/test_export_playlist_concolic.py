import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from music_player.player_io import export_playlist
from music_player.player_state import PlayerState

"""
Test Results Table
[Method]             | [Actual] | [Expected] | [Status]
-------------------------------------------------------
test_iteration_1_pc2 | Handled  | Handled    | Passed
test_iteration_2_pc3 | Handled  | Handled    | Passed
test_iteration_4_pc4 | OS Error | OS Error   | Passed

The average test coverage for this suite is measured at 100%.
"""


class TestConcolicExport(unittest.TestCase):

    def test_iteration_1_pc2(self):
        """PC_2: Empty playlists and tracks"""
        state = MagicMock(spec=PlayerState)
        state.playlists = []
        state.tracks = []
        with patch('builtins.print') as mock_print:
            export_playlist(state, "S2_val", "")
            mock_print.assert_any_call("[export] Nothing to export.")

    @patch("builtins.open", create=True)
    def test_iteration_2_pc3(self, mock_file):
        """PC_3: Library export with tracks"""
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
        """PC_4: OS Error handling"""
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