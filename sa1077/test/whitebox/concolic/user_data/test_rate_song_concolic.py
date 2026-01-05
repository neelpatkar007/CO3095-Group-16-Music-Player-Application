import unittest
from unittest.mock import Mock, patch
from music_player.user_data import rate_song

class TestConcolicTesting(unittest.TestCase):

    def test_iteration_1_flip_s1(self):
        with patch('builtins.print'):
            rate_song(None, "3")

    def test_iteration_2_flip_s3(self):
        state = Mock(spec=['current_track'])
        state.current_track = None
        with patch('builtins.print') as mocked_print:
            rate_song(state, "3")
            mocked_print.assert_called_with("[rate] No song playing.")

    def test_iteration_3_flip_s4(self):
        state = Mock()
        track = Mock()
        state.current_track = track
        with patch('builtins.print') as mocked_print:
            rate_song(state, "6")
            mocked_print.assert_called_with("[rate] Rating must be a whole number 1-5.")

    def test_iteration_4_flip_s5_s6(self):
        state = Mock()
        track = Mock(spec=['title']) # No 'path'
        state.current_track = track
        state.song_ratings = {}
        with patch('builtins.print'):
            rate_song(state, "3")

    @patch('music_player.user_data._save_current_to_profile')
    def test_iteration_5_terminal_path(self, mock_save):
        state = Mock()
        track = Mock()
        track.path = "track_001"
        track.title = "Concolic Trace"
        state.current_track = track
        state.song_ratings = None # Test lazy-initialisation
        with patch('builtins.print'):
            rate_song(state, "5")
            self.assertEqual(state.song_ratings["track_001"], 5)

if __name__ == '__main__':
    unittest.main()