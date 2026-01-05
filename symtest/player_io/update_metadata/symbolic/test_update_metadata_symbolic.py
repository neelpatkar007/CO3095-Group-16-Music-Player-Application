import unittest
from unittest.mock import MagicMock, patch
from music_player.player_io import update_metadata

class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.state = MagicMock()
        self.track = MagicMock()
        self.track.path = "test.mp3"
        self.state.library_tracks = [self.track]

    def test_pc1_empty_idx(self):
        result = update_metadata(self.state, "", "title", "New")
        self.assertIsNone(result)

    def test_pc2_invalid_idx(self):
        with patch('builtins.print') as mocked_print:
            update_metadata(self.state, "99", "title", "New")
            mocked_print.assert_called_with("[edit] Invalid song number.")

    def test_pc3_empty_val(self):
        with patch('builtins.print') as mocked_print:
            update_metadata(self.state, "1", "title", "")
            mocked_print.assert_called_with("[edit] Error: Value cannot be empty.")

    def test_pc4_wrong_field(self):
        with patch('builtins.print') as mocked_print:
            update_metadata(self.state, "1", "genre", "Rock")
            mocked_print.assert_called_with("[edit] Can only edit 'title' or 'artist'.")

if __name__ == "__main__":
    unittest.main()