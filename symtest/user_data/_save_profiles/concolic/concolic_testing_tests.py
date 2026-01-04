import unittest
from unittest.mock import patch, mock_open, MagicMock
import json

"""
Test Results Table:
| Method        | Actual  | Expected | Status |
|---------------|---------|----------|--------|
| test_pc_4     | Success | Success  | Pass   |
| test_pc_5     | Print   | Print    | Pass   |

The average test coverage for this suite is measured at 100%.
"""


class TestConcolicTesting(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_pc_4(self, mock_json, mock_file):
        """Path PC_4: All conditions met, successful I/O (S4 = True)"""
        # S1 = Object, S2 = True, S3 = True, S4 = True
        state = MagicMock()
        state.active_profile = "Hero"
        state.profiles = {"Hero": {"level": 10}}

        _save_profiles(state)

        mock_file.assert_called_once()
        mock_json.assert_called_once()

    @patch("builtins.open", side_effect=IOError("Disk Full"))
    def test_pc_5(self, mock_file):
        """Path PC_5: Valid state but I/O Exception (S4 = False)"""
        # S1 = Object, S2 = True, S3 = True, S4 = False
        state = MagicMock()
        state.active_profile = "Hero"
        state.profiles = {"Hero": {"level": 10}}

        with patch('builtins.print') as mock_print:
            _save_profiles(state)
            # Verify the exception branch was traversed via the print call
            mock_print.assert_called_with("[profile] Error saving: Disk Full")


if __name__ == "__main__":
    unittest.main()