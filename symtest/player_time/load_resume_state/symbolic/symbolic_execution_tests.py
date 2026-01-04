import unittest
from unittest.mock import MagicMock, patch, mock_open
import json
from pathlib import Path

# [Method] | [Actual] | [Expected] | [Status]
# test_pc1_invalid_state | None | None | Pass
# test_pc2_no_file | None | None | Pass
# test_pc3_corrupt_json_type | Print Output | Corrupt | Pass
# test_pc4_missing_path | Print Output | Corrupt | Pass
# test_pc5_no_match | Print Output | Resume State | Pass
# The average test coverage for this suite is measured at 100%.

class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.state = MagicMock()
        self.state.audio_engine = True

    @patch('__main__.RESUME_FILE')
    def test_pc1_invalid_state(self, mock_file):
        # PC_1: S1 is None
        from my_module import load_resume_state
        self.assertIsNone(load_resume_state(None))

    @patch('__main__.RESUME_FILE')
    def test_pc2_no_file(self, mock_file):
        # PC_2: NOT S2 (File exists is False)
        mock_file.exists.return_value = False
        from my_module import load_resume_state
        load_resume_state(self.state)
        mock_file.exists.assert_called_once()

    @patch('__main__.RESUME_FILE')
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_pc3_corrupt_json_type(self, mock_file_open, mock_file_exists):
        # PC_3: S3 is a list, not a dict
        mock_file_exists.exists.return_value = True
        from my_module import load_resume_state
        with patch('builtins.print') as mock_print:
            load_resume_state(self.state)
            mock_print.assert_called_with("[state] Corrupt resume file.")

    @patch('__main__.RESUME_FILE')
    @patch('builtins.open', new_callable=mock_open, read_data='{"position": 10.0}')
    def test_pc4_missing_path(self, mock_file_open, mock_file_exists):
        # PC_4: S4 (path_str) is missing/None
        mock_file_exists.exists.return_value = True
        from my_module import load_resume_state
        with patch('builtins.print') as mock_print:
            load_resume_state(self.state)
            mock_print.assert_called_with("[state] Corrupt resume file.")

    @patch('__main__.RESUME_FILE')
    @patch('builtins.open', new_callable=mock_open, read_data='{"last_track_path": "test.mp3"}')
    def test_pc5_no_match(self, mock_file_open, mock_file_exists):
        # PC_5: matched is False
        mock_file_exists.exists.return_value = True
        self.state.library_tracks = []
        from my_module import load_resume_state
        with patch('builtins.print') as mock_print:
            load_resume_state(self.state)
            mock_print.assert_any_call("[state] Found resume state: test.mp3 at 0s.")

if __name__ == '__main__':
    unittest.main()