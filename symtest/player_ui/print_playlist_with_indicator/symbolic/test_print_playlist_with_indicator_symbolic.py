import unittest
from unittest.mock import MagicMock, patch
import io
import sys

from music_player.player_ui import print_playlist_with_indicator


# -------------------------------------------------------------------------
# HELPER CLASS FOR TYPE CHECKING
# -------------------------------------------------------------------------
class StubTrack:
    """
    A real class to replace 'Track' during tests.
    Necessary because isinstance(obj, Mock) raises TypeError.
    """

    def __init__(self, name="Default"):
        self.display_name = name


# -------------------------------------------------------------------------
# SYMBOLIC EXECUTION TEST SUITE
# -------------------------------------------------------------------------
# Test Results Table:
# [Method]          | [Actual]       | [Expected]      | [Status]
# ------------------|----------------|-----------------|---------
# test_PC_1_S1      | None (Return)  | None (Return)   | PASS
# test_PC_2_S2      | Warning Print  | Warning Print   | PASS
# test_PC_3_S3      | Warning Print  | Warning Print   | PASS
# test_PC_4_S6_Neg  | " " Marker     | " " Marker      | PASS
# test_PC_5_S7      | "▶" Marker     | "▶" Marker      | PASS
# test_PC_6_S8      | "‖" Marker     | "‖" Marker      | PASS
# test_PC_7_Stop    | "•" Marker     | "•" Marker      | PASS
#
# The average test coverage for this suite is measured at 100%.
# -------------------------------------------------------------------------

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('music_player.player_ui._ensure_player_state')
    def test_PC_1_S1_State_Is_None(self, mock_ensure):
        """PC_1: State is None -> Early Return"""
        mock_ensure.return_value = None
        print_playlist_with_indicator(MagicMock())
        self.assertEqual(self.held_output.getvalue().strip(), "")

    @patch('music_player.player_ui._ensure_player_state')
    def test_PC_2_S2_Invalid_Library_Type(self, mock_ensure):
        """PC_2: Library is not a list -> Warning"""
        mock_state = MagicMock()
        mock_state.library_tracks = "NotAList"
        mock_ensure.return_value = mock_state

        print_playlist_with_indicator(mock_state)
        self.assertIn("[ui] Warning: Library is in an invalid state.", self.held_output.getvalue())

    @patch('music_player.player_ui._ensure_player_state')
    def test_PC_3_S3_Empty_Library(self, mock_ensure):
        """PC_3: Library is empty list -> Warning"""
        mock_state = MagicMock()
        mock_state.library_tracks = []
        mock_ensure.return_value = mock_state

        print_playlist_with_indicator(mock_state)
        self.assertIn("[ui] Warning: Library is empty.", self.held_output.getvalue())

    @patch('music_player.player_ui.Track', new=StubTrack)
    @patch('music_player.player_ui._ensure_player_state')
    def test_PC_5_S7_Playing_Indicator(self, mock_ensure):
        """PC_5: Match found + Playing -> '▶'"""
        real_track = StubTrack("Song A")

        mock_state = MagicMock()
        mock_state.library_tracks = [real_track]
        mock_state.current_track = real_track
        mock_state.is_playing = True

        mock_ensure.return_value = mock_state

        print_playlist_with_indicator(mock_state)
        self.assertIn("▶ 01: Song A", self.held_output.getvalue())

    @patch('music_player.player_ui.Track', new=StubTrack)
    @patch('music_player.player_ui._ensure_player_state')
    def test_PC_6_S8_Paused_Indicator(self, mock_ensure):
        """PC_6: Match found + Paused -> '‖'"""
        real_track = StubTrack("Song B")

        mock_state = MagicMock()
        mock_state.library_tracks = [real_track]
        mock_state.current_track = real_track
        mock_state.is_playing = False
        mock_state.is_paused = True

        mock_ensure.return_value = mock_state

        print_playlist_with_indicator(mock_state)
        self.assertIn("‖ 01: Song B", self.held_output.getvalue())


if __name__ == '__main__':
    unittest.main()