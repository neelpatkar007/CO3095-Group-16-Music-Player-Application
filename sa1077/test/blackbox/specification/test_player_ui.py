import unittest
from unittest.mock import MagicMock, patch
import io
import sys
from music_player import player_ui
from music_player.player_state import PlayerState
from music_player.library import Track

class TestPlayerUISpec(unittest.TestCase):
    """
    Black-Box Specification Tests for player_ui.py.
    Testing Tool: Python unittest + unittest.mock + sys + io.
    Test Technique: Black-Box Specification Testing
    Source: playerUI.txt TSL Generated Test Frames
    """
    def setUp(self):
        self.captured_output = io.StringIO()
        self.sys_stdout = sys.stdout
        sys.stdout = self.captured_output
        self.mock_state = MagicMock(spec=PlayerState)
        self.mock_state.current_track = MagicMock(spec=Track)
        self.mock_state.current_track.display_name = "Song"
        self.mock_state.current_track.duration_seconds = 60

    def tearDown(self):
        sys.stdout = self.sys_stdout

    def get_output(self):
        return self.captured_output.getvalue().strip()

    @patch("music_player.player_ui.format_mm_ss", return_value="01:00")
    def test_print_now_playing_states(self, _):
        """
        Expected Result: Prints correct status prefix Playing/Paused/Stopped or No track selected.
        Actual Result: Passed.
        """
        scenarios = [
            (True, False, "Playing"),
            (False, True, "Paused"),
            (False, False, "Stopped")
        ]
        for playing, paused, label in scenarios:
            self.mock_state.is_playing = playing
            self.mock_state.is_paused = paused
            player_ui.print_now_playing(self.mock_state)
            self.assertIn(f"[ui] {label}: Song [01:00]", self.get_output())
            self.captured_output.truncate(0);
            self.captured_output.seek(0)  # Reset buffer

        # Case: No track selected
        self.mock_state.current_track = None
        player_ui.print_now_playing(self.mock_state)
        self.assertIn("[ui] No track selected.", self.get_output())

    @patch("music_player.player_ui.render_progress_bar", return_value="|||...")
    @patch("music_player.player_ui.get_progress", return_value=(30, 60))
    @patch("music_player.player_ui.format_mm_ss", side_effect=["00:30", "01:00"])
    def test_print_progress_features(self, mock_fmt, mock_prog, mock_render):
        """
        Expected Result: Prints progress timestamps and progress bar.
        Actual Result: Passed.
        """
        player_ui.print_progress(self.mock_state)
        self.assertIn("[ui] Progress: 00:30/01:00", self.get_output())

        player_ui.print_progress_bar(self.mock_state)
        self.assertIn("[ui] |||...", self.get_output())