import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
import sys
from music_player.player_queue import show_queue

class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_PC_1_invalid_input(self):

        show_queue(None)
        self.assertEqual(self.captured_output.getvalue(), "")

        show_queue(12345)
        self.assertEqual(self.captured_output.getvalue(), "")

    @patch('music_player.player_queue._get_tracks_safe')
    def test_PC_2_end_of_queue(self, mock_get_tracks):

        state = MagicMock()

        mock_get_tracks.return_value = []

        state.current_index = 0
        state.history = []

        show_queue(state)
        output = self.captured_output.getvalue()
        self.assertIn("(End of queue)", output)

    @patch('music_player.player_queue._get_tracks_safe')
    def test_PC_3_is_playing(self, mock_get_tracks):

        state = MagicMock()

        track = MagicMock()
        track.display_name = "Symphony No. 5"
        mock_get_tracks.return_value = [track]

        state.current_index = 0

        state.is_playing = True

        state.is_paused = False

        show_queue(state)
        output = self.captured_output.getvalue()

        self.assertIn("▶ 1. Symphony No. 5", output)

    @patch('music_player.player_queue._get_tracks_safe')
    def test_PC_4_is_paused(self, mock_get_tracks):
        state = MagicMock()
        track = MagicMock()
        track.display_name = "Adagio for Strings"
        mock_get_tracks.return_value = [track]

        state.current_index = 0

        state.is_playing = False

        state.is_paused = True

        show_queue(state)
        output = self.captured_output.getvalue()

        self.assertIn("‖ 1. Adagio for Strings", output)

    @patch('music_player.player_queue._get_tracks_safe')
    def test_PC_5_default_marker_and_shuffle(self, mock_get_tracks):
        state = MagicMock()
        track = MagicMock()
        track.display_name = "Bohemian Rhapsody"
        mock_get_tracks.return_value = [track]

        state.current_index = 0

        state.is_playing = False
        state.is_paused = False

        state.shuffle_active = True

        show_queue(state)
        output = self.captured_output.getvalue()

        self.assertIn("• 1. Bohemian Rhapsody", output)
        self.assertIn("Shuffle is ON", output)


def _get_tracks_safe(state):
    return []


if __name__ == '__main__':
    unittest.main()