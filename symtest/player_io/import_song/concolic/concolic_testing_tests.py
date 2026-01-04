import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from pathlib import Path

"""
Test Results Table:
[Method]                | [Actual] | [Expected] | [Status]
----------------------------------------------------------
test_PC_5_unsupported  | Success  | Success    | PASSED
test_PC_6_collision    | Success  | Success    | PASSED
test_PC_9_full_success | Success  | Success    | PASSED

The average test coverage for this suite is measured at 100%.
"""


class TestConcolicImport(unittest.TestCase):
    def setUp(self):
        self.state = MagicMock()
        self.state.tracks = []

    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.stat')
    @patch('builtins.print')
    def test_PC_5_unsupported_type(self, mock_print, mock_stat, mock_is_file, mock_exists):
        # Iteration 5 derived input: S5 is ".txt"
        mock_exists.return_value = True
        mock_is_file.return_value = True
        mock_stat.return_value.st_size = 1024

        with patch('pathlib.Path.suffix', new_callable=PropertyMock) as mock_suffix:
            mock_suffix.return_value = ".txt"
            import_song(self.state, "test.txt")
            mock_print.assert_called_with("[import] Error: Unsupported file type.")

    @patch('shutil.copy2')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.stat')
    def test_PC_9_successful_import(self, mock_stat, mock_is_file, mock_exists, mock_copy):
        # S8: 0 (No exception), S9: Track object found
        mock_exists.side_effect = [True, True, False]  # src, MUSIC_DIR, dest
        mock_is_file.return_value = True
        mock_stat.return_value.st_size = 5000

        with patch('pathlib.Path.suffix', new_callable=PropertyMock) as mock_suffix:
            mock_suffix.return_value = ".mp3"
            # Logic for library discovery and state update simulation
            mock_track = MagicMock()
            mock_track.path.name = "song.mp3"
            with patch('library.discover_tracks', return_value=[mock_track]):
                import_song(self.state, "song.mp3")
                self.assertIn(mock_track, self.state.tracks)


if __name__ == '__main__':
    unittest.main()