import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import next_track

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()
        self.state.history = []
        self.state.current_index = 0
        self.state.position_seconds = 10.0
        self.state.is_playing = False
        self.state.is_paused = False
        self.state.loop_mode = "off"
        self.state.shuffle_active = False

    def tearDown(self):
        self.state = None

    @patch('builtins.print')
    def test_PC1_invalid_state(self, mock_print):
        next_track(None)
        mock_print.assert_called_with("[queue] Error: State is invalid.")

        next_track(123)
        mock_print.assert_called_with("[queue] Error: State is invalid.")

    @patch('music_player.player_queue._get_tracks_safe')
    @patch('builtins.print')
    def test_PC2_no_tracks(self, mock_print, mock_get_tracks):
        mock_get_tracks.return_value = []

        next_track(self.state)
        mock_print.assert_called_with("[queue] No tracks available.")

    @patch('music_player.player_queue._get_tracks_safe')
    def test_PC3_loop_one(self, mock_get_tracks):
        t1, t2 = MagicMock(), MagicMock()
        mock_get_tracks.return_value = [t1, t2]

        self.state.current_index = 0
        self.state.loop_mode = "one"
        self.state.shuffle_active = True

        next_track(self.state)

        self.assertEqual(self.state.current_index, 0, "Index should remain unchanged in loop 'one'.")
        self.assertEqual(self.state.position_seconds, 0.0, "Position should reset.")

    @patch('music_player.player_queue._get_tracks_safe')
    @patch('random.randint')
    def test_PC4_shuffle(self, mock_randint, mock_get_tracks):
        t1, t2, t3 = MagicMock(), MagicMock(), MagicMock()
        mock_get_tracks.return_value = [t1, t2, t3]

        self.state.current_index = 0
        self.state.loop_mode = "off"
        self.state.shuffle_active = True

        mock_randint.return_value = 2
        next_track(self.state)

        self.assertEqual(self.state.current_index, 2, "Shuffle should select random index.")

    @patch('music_player.player_queue._get_tracks_safe')
    @patch('builtins.print')
    def test_PC5_sequential_stop(self, mock_print, mock_get_tracks):
        t1, t2 = MagicMock(), MagicMock()
        mock_get_tracks.return_value = [t1, t2]

        self.state.current_index = 1  # At end
        self.state.loop_mode = "off"
        self.state.shuffle_active = False
        self.state.is_playing = True

        next_track(self.state)

        mock_print.assert_called_with("[queue] End of playlist.")
        self.assertFalse(self.state.is_playing, "Playback should stop at end of list.")

    @patch('music_player.player_queue._get_tracks_safe')
    def test_PC7_sequential_next(self, mock_get_tracks):
        t1, t2 = MagicMock(), MagicMock()
        t2.display_name = "Track 2"
        mock_get_tracks.return_value = [t1, t2]

        self.state.current_index = 0
        self.state.loop_mode = "off"
        self.state.shuffle_active = False

        next_track(self.state)

        self.assertEqual(self.state.current_index, 1, "Should increment to next index.")


if __name__ == "__main__":
    unittest.main()
