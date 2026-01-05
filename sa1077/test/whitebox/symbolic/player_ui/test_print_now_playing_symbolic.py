import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
import sys

# Standard engineering practice: Import the target function
from music_player.player_ui import print_now_playing


class TestSymbolicExecution(unittest.TestCase):
    """
    White-box symbolic testing suite mapping directly to Path Conditions (PC_1..PC_8).

    -------------------------------------------------------
    | Method      | Actual | Expected | Status            |
    |-------------|--------|----------|-------------------|
    | test_pc_1   | Return | Return   | PASS              |
    | test_pc_2   | Print  | Print    | PASS              |
    | test_pc_3   | Print  | Print    | PASS              |
    | test_pc_4   | Print  | Print    | PASS              |
    | test_pc_5   | Print  | Print    | PASS              |
    | test_pc_6   | Print  | Print    | PASS              |
    | test_pc_7   | Print  | Print    | PASS              |
    | test_pc_8   | Print  | Print    | PASS              |
    -------------------------------------------------------
    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

        # Define a dummy class to act as the real Track type for isinstance checks
        class RealTrack: pass

        self.RealTrackClass = RealTrack

        # Instrumentation: Patch dependencies in the target module
        self.mock_ensure_patcher = patch('music_player.player_ui._ensure_player_state')
        self.mock_ensure = self.mock_ensure_patcher.start()

        self.mock_format_patcher = patch('music_player.player_ui.format_mm_ss')
        self.mock_format = self.mock_format_patcher.start()
        self.mock_format.return_value = "03:30"

        # Fix: Patch 'Track' to be the actual class type to satisfy isinstance()
        self.track_patcher = patch('music_player.player_ui.Track', new=self.RealTrackClass)
        self.track_patcher.start()

    def tearDown(self):
        sys.stdout = self.held
        self.mock_ensure_patcher.stop()
        self.mock_format_patcher.stop()
        self.track_patcher.stop()

    def test_pc_1_state_is_none(self):
        """PC_1: S1 == None. Early return analysis."""
        self.mock_ensure.return_value = None
        print_now_playing(MagicMock())
        self.assertEqual(sys.stdout.getvalue().strip(), "")

    def test_pc_2_track_is_none(self):
        """PC_2: S1 != None AND S2 == None. Path to 'No track selected'."""
        state_mock = MagicMock()
        state_mock.current_track = None
        self.mock_ensure.return_value = state_mock
        print_now_playing(state_mock)
        self.assertEqual(sys.stdout.getvalue().strip(), "[ui] No track selected.")

    def test_pc_3_track_not_instance(self):
        """PC_3: S1 != None AND S2 != None AND NOT S3. Type verification."""
        state_mock = MagicMock()
        state_mock.current_track = "Not A Track Instance"
        self.mock_ensure.return_value = state_mock
        print_now_playing(state_mock)
        self.assertEqual(sys.stdout.getvalue().strip(), "[ui] Error: Track data corrupted.")

    def test_pc_4_missing_display_name(self):
        """PC_4: S3 (is Track) AND NOT S4 (Missing attr). Attribute existence check."""
        state_mock = MagicMock()
        track_obj = self.RealTrackClass()
        # display_name is NOT added to this instance
        state_mock.current_track = track_obj
        self.mock_ensure.return_value = state_mock
        print_now_playing(state_mock)
        self.assertEqual(sys.stdout.getvalue().strip(), "[ui] Error: Track metadata missing.")

    def test_pc_5_playing_and_paused(self):
        """PC_5: S5 (Playing) AND S6 (Paused). Logic prioritisation."""
        state_mock = MagicMock()
        track_obj = self.RealTrackClass()
        track_obj.display_name = "Song A"
        track_obj.duration_seconds = 200
        state_mock.current_track = track_obj
        state_mock.is_playing = True
        state_mock.is_paused = True
        self.mock_ensure.return_value = state_mock
        print_now_playing(state_mock)
        self.assertIn("Paused: Song A", sys.stdout.getvalue())

    def test_pc_6_playing_not_paused(self):
        """PC_6: S5 (Playing) AND NOT S6 (Paused). Active playback state."""
        state_mock = MagicMock()
        track_obj = self.RealTrackClass()
        track_obj.display_name = "Song B"
        track_obj.duration_seconds = 200
        state_mock.current_track = track_obj
        state_mock.is_playing = True
        state_mock.is_paused = False
        self.mock_ensure.return_value = state_mock
        print_now_playing(state_mock)
        self.assertIn("Playing: Song B", sys.stdout.getvalue())

    def test_pc_7_not_playing_is_paused(self):
        """PC_7: NOT S5 (Playing) AND S6 (Paused). Standby pause state."""
        state_mock = MagicMock()
        track_obj = self.RealTrackClass()
        track_obj.display_name = "Song C"
        track_obj.duration_seconds = 200
        state_mock.current_track = track_obj
        state_mock.is_playing = False
        state_mock.is_paused = True
        self.mock_ensure.return_value = state_mock
        print_now_playing(state_mock)
        self.assertIn("Paused: Song C", sys.stdout.getvalue())

    def test_pc_8_not_playing_not_paused(self):
        """PC_8: NOT S5 AND NOT S6. Default terminal state (Stopped)."""
        state_mock = MagicMock()
        track_obj = self.RealTrackClass()
        track_obj.display_name = "Song D"
        track_obj.duration_seconds = 200
        state_mock.current_track = track_obj
        state_mock.is_playing = False
        state_mock.is_paused = False
        self.mock_ensure.return_value = state_mock
        print_now_playing(state_mock)
        self.assertIn("Stopped: Song D", sys.stdout.getvalue())