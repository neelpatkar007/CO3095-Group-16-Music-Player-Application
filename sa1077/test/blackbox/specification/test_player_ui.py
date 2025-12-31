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

    def test_playlist_warnings(self):
        """
        Expected Result: Prints appropriate warnings for all invalid playlist states.
        Actual Result: Passed.
        """
        scenarios = [
            ("Not a list", "invalid state"),
            (["Not a Track"], "invalid state"),
            ([], "empty"),
            ([MagicMock(spec=Track, display_name="")], "missing titles")
        ]
        for lib, error_msg in scenarios:
            self.mock_state.library_tracks = lib
            player_ui.print_playlist_with_indicator(self.mock_state)
            self.assertIn(error_msg, self.get_output())
            self.captured_output.truncate(0); self.captured_output.seek(0)

    def test_playlist_indicators_and_single_note(self):
            """
            Expected Result: Prints note for single track libraries and correct indicators for track states.
            Actual Result: Passed
            """
            t1, t2 = MagicMock(spec=Track, display_name="S1"), MagicMock(spec=Track, display_name="S2")
            self.mock_state.library_tracks = [t1]

            # Single track note
            player_ui.print_playlist_with_indicator(self.mock_state)
            self.assertIn("Note: Only one track", self.get_output())
            self.captured_output.truncate(0);
            self.captured_output.seek(0)

            # Indicator tests
            self.mock_state.library_tracks = [t1, t2]
            self.mock_state.current_track = t1

            indicator_map = [(True, False, "▶"), (False, True, "‖"), (False, False, "•")]
            for playing, paused, symbol in indicator_map:
                self.mock_state.is_playing = playing
                self.mock_state.is_paused = paused

                player_ui.print_playlist_with_indicator(self.mock_state)
                self.assertIn(f"{symbol} 01: S1", self.get_output())
                self.captured_output.truncate(0);
                self.captured_output.seek(0)

    if __name__ == '__main__':
        unittest.main()