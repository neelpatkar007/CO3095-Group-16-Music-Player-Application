import unittest
from unittest.mock import Mock, patch
from music_player.user_data import rate_song

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = Mock()
        self.track = Mock()

    def test_pc1_state_is_none(self):
        with patch('builtins.print') as mocked_print:
            rate_song(None, "3")
            mocked_print.assert_called_with("[rate] No song playing.")

    def test_pc2_track_is_none(self):
        self.state.current_track = None
        with patch('builtins.print') as mocked_print:
            rate_song(self.state, "3")
            mocked_print.assert_called_with("[rate] No song playing.")

    def test_pc3_invalid_rating(self):
        self.state.current_track = self.track
        with patch('builtins.print') as mocked_print:
            rate_song(self.state, "6")
            mocked_print.assert_called_with("[rate] Rating must be a whole number 1-5.")

    def test_pc4_missing_attributes(self):
        self.state.current_track = self.track
        del self.track.path
        self.state.song_ratings = {}
        result = rate_song(self.state, "3")
        self.assertIsNone(result)

    @patch('music_player.user_data._save_current_to_profile')
    def test_pc5_successful_rating(self, mock_save):
        self.track.path = "/music/song.mp3"
        self.track.title = "Test Song"
        self.state.current_track = self.track
        self.state.song_ratings = {}
        with patch('builtins.print') as mocked_print:
            rate_song(self.state, "3")
            self.assertEqual(self.state.song_ratings["/music/song.mp3"], 3)
            mocked_print.assert_any_call("[rate] Rated 'Test Song' 3/5 stars.")

if __name__ == '__main__':
    unittest.main()