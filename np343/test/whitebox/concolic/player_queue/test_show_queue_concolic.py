import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
import sys
from music_player.player_queue import show_queue
class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.captured_output = StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_iteration_1_invalid_seed(self):
        show_queue(None)
        self.assertEqual(self.captured_output.getvalue(), "")

    @patch('music_player.player_queue._get_tracks_safe')
    def test_iteration_2_boundary_flip(self, mock_get_tracks):
        state = MagicMock()
        mock_get_tracks.return_value = []
        state.current_index = 0


        show_queue(state)
        self.assertIn("(End of queue)", self.captured_output.getvalue())

    @patch('music_player.player_queue._get_tracks_safe')
    def test_iteration_3_playing_flip(self, mock_get_tracks):
        state = MagicMock()
        track = MagicMock()
        track.display_name = "Track A"
        mock_get_tracks.return_value = [track]
        state.current_index = 0

        state.is_playing = True

        show_queue(state)
        self.assertIn("▶", self.captured_output.getvalue())

    @patch('music_player.player_queue._get_tracks_safe')
    def test_iteration_4_paused_flip(self, mock_get_tracks):
        state = MagicMock()
        track = MagicMock()
        track.display_name = "Track B"
        mock_get_tracks.return_value = [track]
        state.current_index = 0


        state.is_playing = False
        state.is_paused = True

        show_queue(state)
        self.assertIn("‖", self.captured_output.getvalue())

    @patch('music_player.player_queue._get_tracks_safe')
    def test_iteration_5_shuffle_flip(self, mock_get_tracks):
        state = MagicMock()
        track = MagicMock()
        track.display_name = "Track C"
        mock_get_tracks.return_value = [track]
        state.current_index = 0

        state.is_playing = False
        state.is_paused = False
        state.shuffle_active = True

        show_queue(state)
        output = self.captured_output.getvalue()
        self.assertIn("•", output)
        self.assertIn("Shuffle is ON", output)



def _get_tracks_safe(state):
    return []


if __name__ == '__main__':
    unittest.main()