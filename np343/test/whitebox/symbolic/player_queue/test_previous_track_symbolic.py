import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import previous_track

class PlayerState:
    def __init__(self):
        self.current_index = 0
        self.loop_mode = "off"
        self.shuffle_active = False
        self.history = []
        self.is_playing = False
        self.is_paused = False
        self.position_seconds = 0.0
        self.audio_engine = MagicMock()


class Track:
    def __init__(self, name="Track", path="path/to/file"):
        self.display_name = name
        self.path = path


class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.state = PlayerState()
        self.track1 = Track("Track 1")
        self.track2 = Track("Track 2")
        self.tracks = [self.track1, self.track2]

    def test_PC_1_invalid_state(self):
        result = previous_track(None)
        self.assertIsNone(result)

        result = previous_track(123)
        self.assertIsNone(result)

    @patch('builtins.print')
    def test_PC_2_no_tracks(self, mock_print):
        with patch('music_player.player_queue._get_tracks_safe', return_value=None):
            previous_track(self.state)
            self.assertTrue(any("No tracks available" in str(c) for c in mock_print.call_args_list))

    @patch('builtins.print')
    def test_PC_3_empty_library(self, mock_print):
        with patch('music_player.player_queue._get_tracks_safe', return_value=[]):
            previous_track(self.state)
            self.assertTrue(any("[queue] No tracks available." in str(c) for c in mock_print.call_args_list))

    @patch('music_player.player_queue._get_tracks_safe')
    def test_PC_5_loop_one_playing(self, mock_get_tracks):
        mock_get_tracks.return_value = self.tracks
        self.state.loop_mode = "one"
        self.state.current_index = 1
        self.state.is_playing = True

        previous_track(self.state)

        self.assertEqual(self.state.current_index, 1)
        self.state.audio_engine.play.assert_called()

    @patch('music_player.player_queue._get_tracks_safe')
    def test_PC_6_shuffle_paused(self, mock_get_tracks):
        mock_get_tracks.return_value = self.tracks
        self.state.shuffle_active = True
        self.state.history = [self.track1]
        self.state.current_index = 1
        self.state.is_paused = True  # S9

        previous_track(self.state)

        self.assertEqual(self.state.current_index, 0)
        self.assertFalse(self.state.is_paused)

    @patch('music_player.player_queue._get_tracks_safe')
    def test_PC_7_normal_stopped(self, mock_get_tracks):
        mock_get_tracks.return_value = self.tracks
        self.state.loop_mode = "off"
        self.state.current_index = 1
        self.state.is_playing = False
        self.state.is_paused = False

        previous_track(self.state)

        self.assertEqual(self.state.current_index, 0)
