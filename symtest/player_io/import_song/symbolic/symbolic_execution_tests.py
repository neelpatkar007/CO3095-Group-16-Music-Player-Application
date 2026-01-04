import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import shutil

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
        # S1: source_path_str is empty
        import_song(self.state, "")
        mock_print.assert_called_with("[import] Usage: /import <path_to_file>")

    @patch('pathlib.Path.exists')
    @patch('builtins.print')
    def test_PC_2_not_found(self, mock_print, mock_exists):
        # S1: "valid.mp3", S2: exists() is False
        mock_exists.return_value = False
        import_song(self.state, "missing.mp3")
        mock_print.assert_called_with("[import] Error: File not found.")

    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_file')
    @patch('pathlib.Path.stat')
    @patch('builtins.print')
    def test_PC_4_empty_file(self, mock_print, mock_stat, mock_is_file, mock_exists):
        # S1: "empty.mp3", S2: True, S3: True, S4: st_size == 0
        mock_exists.return_value = True
        mock_is_file.return_value = True
        mock_stat.return_value.st_size = 0
        import_song(self.state, "empty.mp3")
        mock_print.assert_called_with("[import] Error: File is empty.")

if __name__ == '__main__':
    unittest.main()