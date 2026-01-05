import unittest
from unittest.mock import MagicMock, patch, PropertyMock, mock_open
from pathlib import Path
from music_player.player_io import import_song

class TestConcolicImport(unittest.TestCase):
    def setUp(self):
        self.state = MagicMock()
        self.state.tracks = []
        self.state.library_tracks = []

    @patch('music_player.player_io.SUPPORTED_EXTENSIONS', ['.mp3', '.wav', '.flac'])
    @patch('builtins.print')
    def test_PC_5_unsupported_type(self, mock_print):
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        mock_path.is_file.return_value = True
        mock_path.stat.return_value.st_size = 1024
        mock_path.suffix = ".txt"
        mock_path.name = "test.txt"

        with patch('music_player.player_io.Path', return_value=mock_path):
            import_song(self.state, "test.txt")
            mock_print.assert_called_with("[import] Error: Unsupported file type.")

    @patch('music_player.player_io.SUPPORTED_EXTENSIONS', ['.mp3', '.wav', '.flac'])
    @patch('music_player.player_io.library.discover_tracks')
    @patch('shutil.copy2')
    @patch('builtins.print')
    def test_PC_9_successful_import(self, mock_print, mock_copy, mock_discover):
        mock_src = MagicMock(spec=Path)
        mock_src.exists.return_value = True
        mock_src.is_file.return_value = True
        mock_src.stat.return_value.st_size = 5000
        mock_src.suffix = ".mp3"
        mock_src.name = "song.mp3"

        mock_dest = MagicMock(spec=Path)
        mock_dest.exists.return_value = False

        mock_music_dir = MagicMock(spec=Path)
        mock_music_dir.exists.return_value = True
        mock_music_dir.__truediv__.return_value = mock_dest

        mock_track = MagicMock()
        mock_track.display_name = "song"
        mock_track.path.name = "song.mp3"
        mock_discover.return_value = [mock_track]

        with patch('music_player.player_io.Path') as mock_path_class:
            mock_path_class.return_value = mock_src
            with patch('music_player.player_io.MUSIC_DIR', mock_music_dir):
                import_song(self.state, "/path/to/song.mp3")
                self.assertIn(mock_track, self.state.tracks)
                mock_copy.assert_called_once()


if __name__ == '__main__':
    unittest.main()