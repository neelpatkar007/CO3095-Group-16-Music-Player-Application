import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
import sys

from music_player.player_ui import print_now_playing


class TestConcolicTesting(unittest.TestCase):

    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

        class RealTrack: pass

        self.RealTrackClass = RealTrack

        self.mock_ensure_patcher = patch('music_player.player_ui._ensure_player_state')
        self.mock_ensure = self.mock_ensure_patcher.start()

        self.mock_format_patcher = patch('music_player.player_ui.format_mm_ss')
        self.mock_format = self.mock_format_patcher.start()
        self.mock_format.return_value = "00:00"

        self.track_patcher = patch('music_player.player_ui.Track', new=self.RealTrackClass)
        self.track_patcher.start()

    def tearDown(self):
        sys.stdout = self.held
        self.mock_ensure_patcher.stop()
        self.mock_format_patcher.stop()
        self.track_patcher.stop()

    def test_iterations_structural(self):
        self.mock_ensure.return_value = None
        print_now_playing(MagicMock())
        self.assertEqual(sys.stdout.getvalue().strip(), "")

        sys.stdout = StringIO()
        s2 = MagicMock();
        s2.current_track = None
        self.mock_ensure.return_value = s2
        print_now_playing(s2)
        self.assertEqual(sys.stdout.getvalue().strip(), "[ui] No track selected.")

        sys.stdout = StringIO()
        s3 = MagicMock();
        s3.current_track = "Invalid Type"
        self.mock_ensure.return_value = s3
        print_now_playing(s3)
        self.assertEqual(sys.stdout.getvalue().strip(), "[ui] Error: Track data corrupted.")

    def test_iterations_status(self):

        def run_status(playing, paused):
            sys.stdout = StringIO()
            state = MagicMock()
            track = self.RealTrackClass()
            track.display_name = "Test"
            track.duration_seconds = 10
            state.current_track = track
            state.is_playing = playing
            state.is_paused = paused
            self.mock_ensure.return_value = state
            print_now_playing(state)
            return sys.stdout.getvalue()

        self.assertIn("Paused:", run_status(True, True))  # PC_5
        self.assertIn("Playing:", run_status(True, False))  # PC_6
        self.assertIn("Paused:", run_status(False, True))  # PC_7
        self.assertIn("Stopped:", run_status(False, False))  # PC_8

    def test_edge_cases_data_flow(self):
        state = MagicMock()
        track = self.RealTrackClass()
        track.display_name = "Edge"
        state.current_track = track
        self.mock_ensure.return_value = state

        track.duration_seconds = None
        print_now_playing(state)
        self.mock_format.assert_any_call(0.0)

        track.duration_seconds = -1.0
        print_now_playing(state)
        self.mock_format.assert_any_call(0.0)