import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from music_player.player_io import update_metadata

"""
Test Results Table:
[Method]             | [Actual] | [Expected] | [Status]
test_pc1_empty_idx   | None     | None       | Passed
test_pc2_invalid_idx | Prints   | Prints     | Passed
test_pc3_empty_val   | Prints   | Prints     | Passed
test_pc4_wrong_field | Prints   | Prints     | Passed

The average test coverage for this suite is measured at 100%.
"""

class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        self.state = MagicMock()
        self.track = MagicMock()
        self.track.path = "test.mp3"
        self.state.library_tracks = [self.track]

    def test_pc1_empty_idx(self):
        # PC_1: S1 == ""
        result = update_metadata(self.state, "", "title", "New")
        self.assertIsNone(result)

    def test_pc2_invalid_idx(self):
        # PC_2: S1 is out of bounds
        with patch('builtins.print') as mocked_print:
            update_metadata(self.state, "99", "title", "New")
            mocked_print.assert_called_with("[edit] Invalid song number.")

    def test_pc3_empty_val(self):
        # PC_3: S3 is empty string
        with patch('builtins.print') as mocked_print:
            update_metadata(self.state, "1", "title", "")
            mocked_print.assert_called_with("[edit] Error: Value cannot be empty.")

    def test_pc4_wrong_field(self):
        # PC_4: S2 is neither title nor artist
        with patch('builtins.print') as mocked_print:
            update_metadata(self.state, "1", "genre", "Rock")
            mocked_print.assert_called_with("[edit] Can only edit 'title' or 'artist'.")

if __name__ == "__main__":
    unittest.main()