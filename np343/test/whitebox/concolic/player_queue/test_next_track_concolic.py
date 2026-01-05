import unittest
from unittest.mock import MagicMock, patch
from music_player.player_queue import next_track

class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()
        self.state.history = []
        self.state.position_seconds = 10.0
        self.state.is_playing = False
        self.state.is_paused = False
        self.state.audio_engine = MagicMock()
        self.state.current_index = 0
        self.state.loop_mode = "off"
        self.state.shuffle_active = False

    @patch('builtins.print')
    def test_iter_1_bad_S1(self, mock_print):
        next_track(None)
        mock_print.assert_called_with("[queue] Error: State is invalid.")

    @patch('music_player.player_queue._get_tracks_safe')
    @patch('builtins.print')
    def test_iter_2_bad_S2(self, mock_print, mock_get_tracks):
        mock_get_tracks.return_value = []

        next_track(self.state)
        mock_print.assert_called_with("[queue] No tracks available.")

    @patch('music_player.player_queue._get_tracks_safe')
    def test_iter_3_seq_stop(self, mock_get_tracks):
        t1, t2 = MagicMock(), MagicMock()
        mock_get_tracks.return_value = [t1, t2]

        self.state.current_index = 1
        self.state.loop_mode = "off"
        self.state.shuffle_active = False
        self.state.is_playing = True

        next_track(self.state)

        self.assertFalse(self.state.is_playing)
        self.assertEqual(self.state.current_index, 1)

    @patch('music_player.player_queue._get_tracks_safe')
    @patch('builtins.print')
    def test_iter_4_seq_wrap(self, mock_print, mock_get_tracks):
        t1, t2 = MagicMock(), MagicMock()
        t1.display_name = "Track 1"
        mock_get_tracks.return_value = [t1, t2]

        self.state.current_index = 1
        self.state.loop_mode = "all"
        self.state.shuffle_active = False
        self.state.is_playing = True

        next_track(self.state)

        self.assertEqual(self.state.current_index, 0)
        mock_print.assert_called_with("[queue] Wrapped to next: Track 1")

    @patch('music_player.player_queue._get_tracks_safe')
    @patch('builtins.print')
    def test_iter_5_seq_next(self, mock_print, mock_get_tracks):
        t1, t2 = MagicMock(), MagicMock()
        t2.display_name = "Track 2"
        mock_get_tracks.return_value = [t1, t2]

        self.state.current_index = 0
        self.state.loop_mode = "off"
        self.state.shuffle_active = False
        self.state.is_playing = True

        next_track(self.state)

        self.assertEqual(self.state.current_index, 1)
        mock_print.assert_called_with("[queue] Next: Track 2")


if __name__ == "__main__":
    unittest.main()
