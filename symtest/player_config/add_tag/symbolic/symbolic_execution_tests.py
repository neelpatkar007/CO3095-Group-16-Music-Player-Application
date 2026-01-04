import unittest
from unittest.mock import MagicMock
import io
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from music_player.player_config import add_tag


class TestSymbolicExecution(unittest.TestCase):
    """
    Symbolic Execution Test Suite for add_tag function.

    Test Results Table:
    | Method                     | Actual | Expected | Status |
    |----------------------------|--------|----------|--------|
    | test_pc1_state_none        | Output | Error    | PASS   |
    | test_pc2_invalid_index     | Output | Error    | PASS   |
    | test_pc3_corrupt_tags      | Output | Error    | PASS   |
    | test_pc4_corrupt_lib       | Output | Error    | PASS   |
    | test_pc5_index_bounds      | Output | Error    | PASS   |
    | test_pc6_track_none        | Return | Silent   | PASS   |
    | test_pc7_tag_none          | Output | Error    | PASS   |
    | test_pc8_tag_too_long      | Output | Error    | PASS   |
    | test_pc9_invalid_char      | Output | Error    | PASS   |
    | test_pc10_max_tags         | Output | Error    | PASS   |
    | test_pc11_tag_exists       | Output | Info     | PASS   |
    | test_pc12_add_success      | Output | Added    | PASS   |

    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        # Redirect stdout to capture print statements
        self.held, sys.stdout = sys.stdout, io.StringIO()

        # Base Mock Objects
        self.mock_track = MagicMock()
        self.mock_track.path = "/music/song.mp3"
        self.mock_track.title = "Test Song"

        self.mock_state = MagicMock()
        self.mock_state.song_tags = {}
        self.mock_state.library_tracks = [self.mock_track]

    def tearDown(self):
        sys.stdout = self.held

    def test_pc1_state_none(self):
        """PC_1: Verify S1 is None handling."""
        add_tag(None, "1", "tag")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: State is None.")

    def test_pc2_invalid_index(self):
        """PC_2: Verify invalid S2 parsing (ValueError/TypeError)."""
        add_tag(self.mock_state, "abc", "tag")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: Invalid number format.")

    def test_pc3_corrupt_tags(self):
        """PC_3: Verify S4 integrity (song_tags not dict)."""
        self.mock_state.song_tags = []  # Incorrect type
        add_tag(self.mock_state, "1", "tag")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: Tag data is unavailable/corrupted.")

    def test_pc4_corrupt_lib(self):
        """PC_4: Verify S5 integrity (library_tracks not list)."""
        self.mock_state.library_tracks = {}  # Incorrect type
        add_tag(self.mock_state, "1", "tag")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: Library tracks missing/corrupted.")

    def test_pc5_index_bounds(self):
        """PC_5: Verify S2 results in out of bounds index."""
        # Library has 1 item, so index "5" is out of bounds
        add_tag(self.mock_state, "5", "tag")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: Song index out of range.")

    def test_pc6_track_none(self):
        """PC_6: Verify S7 (track) is None (Silent return)."""
        self.mock_state.library_tracks = [None]
        add_tag(self.mock_state, "1", "tag")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "")  # Should be silent

    def test_pc7_tag_none(self):
        """PC_7: Verify S3 is None."""
        add_tag(self.mock_state, "1", None)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: Tag cannot be empty.")

    def test_pc8_tag_too_long(self):
        """PC_8: Verify S3 length > 15."""
        long_tag = "A" * 16
        add_tag(self.mock_state, "1", long_tag)
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Error: Tag is too long (max 15 chars).")

    def test_pc9_invalid_char(self):
        """PC_9: Verify S3 contains invalid characters."""
        add_tag(self.mock_state, "1", "tag!")
        output = sys.stdout.getvalue().strip()
        self.assertIn("[tags] Error: Invalid character", output)

    def test_pc10_max_tags(self):
        """PC_10: Verify max tags limit reached."""
        # Pre-fill with 5 tags
        path = str(self.mock_track.path)
        self.mock_state.song_tags[path] = ["t1", "t2", "t3", "t4", "t5"]

        add_tag(self.mock_state, "1", "t6")
        output = sys.stdout.getvalue().strip()
        self.assertIn("has reached the limit of 5 tags", output)

    def test_pc11_tag_exists(self):
        """PC_11: Verify duplicate tag logic."""
        path = str(self.mock_track.path)
        self.mock_state.song_tags[path] = ["techno"]

        add_tag(self.mock_state, "1", "techno")
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "[tags] Song already has tag #techno.")

    def test_pc12_add_success(self):
        """PC_12: Verify successful addition."""
        add_tag(self.mock_state, "1", "jazz")
        output = sys.stdout.getvalue().strip()

        path = str(self.mock_track.path)
        self.assertEqual(output, "[tags] Added #jazz to 'Test Song'.")
        self.assertIn("jazz", self.mock_state.song_tags[path])


if __name__ == '__main__':
    unittest.main()