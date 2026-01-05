import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
import sys

from music_player.player_ui import print_now_playing


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

        class RealTrack: pass

        self.RealTrackClass = RealTrack

        self.mock_ensure_patcher = patch('music_player.player_ui._ensure_player_state')
        self.mock_ensure = self.mock_ensure_patcher.start()

        self.mock_format_patcher = patch('music_player.player_ui.format_mm_ss')
        self.mock_format = self.mock_format_patcher.start()
        self.mock_format.return_value = "03:30"

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
        state_mock = MagicMock()
        state_mock.current_track = None
        self.mock_ensure.return_value = state_mock
        print_now_playing(state_mock)
        self.assertEqual(sys.stdout.getvalue().strip(), "[ui] No track selected.")

    def test_pc_3_track_not_instance(self):
        state_mock = MagicMock()
        state_mock.current_track = "Not A Track Instance"
        self.mock_ensure.return_value = state_mock
        print_now_playing(state_mock)
        self.assertEqual(sys.stdout.getvalue().strip(), "[ui] Error: Track data corrupted.")

    def test_pc_4_missing_display_name(self):
        state_mock = MagicMock()
        track_obj = self.RealTrackClass()
        state_mock.current_track = track_obj
        self.mock_ensure.return_value = state_mock
        print_now_playing(state_mock)
        self.assertEqual(sys.stdout.getvalue().strip(), "[ui] Error: Track metadata missing.")

    def test_pc_5_playing_and_paused(self):
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