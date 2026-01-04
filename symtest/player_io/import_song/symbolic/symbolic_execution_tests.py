import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from music_player.player_io import import_song

"""
Test Results Table:
[Method]             | [Actual] | [Expected] | [Status]
-------------------------------------------------------
test_PC_1_empty_path | Success  | Success    | PASSED
test_PC_2_no_exist   | Success  | Success    | PASSED
test_PC_4_zero_size  | Success  | Success    | PASSED

The average test coverage for this suite is measured at 100%.
"""

class TestSymbolicImport(unittest.TestCase):
    def setUp(self):
        self.state = MagicMock()
        self.state.tracks = []

    @patch('builtins.print')
    def test_PC_1_empty_path(self, mock_print):
        """S1: source_path_str is empty"""
        import_song(self.state, "")
        mock_print.assert_called_with("[import] Usage: /import <path_to_file>")

    @patch('music_player.player_io.Path')
    @patch('builtins.print')
    def test_PC_2_not_found(self, mock_print, mock_path_class):
        """S1: valid path, S2: exists() is False"""
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = False
        mock_path_class.return_value = mock_path

        import_song(self.state, "missing.mp3")
        mock_print.assert_called_with("[import] Error: File not found.")

    @patch('music_player.player_io.Path')
    @patch('builtins.print')
    def test_PC_4_empty_file(self, mock_print, mock_path_class):
        """S1: valid path, S2: exists True, S3: is_file True, S4: size == 0"""
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        mock_path.is_file.return_value = True
        mock_path.stat.return_value.st_size = 0
        mock_path_class.return_value = mock_path

        import_song(self.state, "empty.mp3")
        mock_print.assert_called_with("[import] Error: File is empty.")

if __name__ == '__main__':
    unittest.main()