import unittest
from unittest.mock import MagicMock, patch

from music_player.player_io import update_metadata
class TestConcolicMetadata(unittest.TestCase):
    def setUp(self):
        self.state = MagicMock()
        self.track = MagicMock()
        self.track.path = MagicMock()
        self.track.title = "Old"
        self.track.artist = "Artist"
        self.state.library_tracks = [self.track]

    @patch('os.access')
    @patch('builtins.print')
    def test_pc5_no_access(self, mock_print, mock_access):
        mock_access.return_value = False
        update_metadata(self.state, "1", "title", "New")
        mock_print.assert_any_call("[edit] Error: No write permission for file.")

    @patch('mutagen.easyid3.EasyID3', side_effect=ImportError)
    @patch('os.access')
    @patch('builtins.print')
    def test_pc6_no_mutagen(self, mock_print, mock_access, mock_easyid3):
        mock_access.return_value = True
        update_metadata(self.state, "1", "title", "New")
        mock_print.assert_any_call("[edit] WARNING: 'mutagen' not installed. Changes will NOT persist after restart.")

    @patch('mutagen.easyid3.EasyID3')
    @patch('os.access')
    @patch('builtins.print')
    def test_pc7_success(self, mock_print, mock_access, mock_easyid3):
        mock_access.return_value = True
        mock_instance = MagicMock()
        mock_easyid3.return_value = mock_instance

        update_metadata(self.state, "1", "title", "New")
        mock_print.assert_any_call("[edit] File tags updated successfully (Persistent).")
        self.assertEqual(self.track.title, "New")
        mock_instance.save.assert_called_once()

if __name__ == "__main__":
    unittest.main()