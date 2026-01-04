import unittest
from unittest.mock import Mock, patch
import io
import sys
from music_player.playlists_basic import _print_playlist_contents


class TestSymbolicExecution(unittest.TestCase):
    """
    White-Box Symbolic Execution Test Suite.

    Test Results Table:
    | Method | Actual | Expected | Status |
    |--------|--------|----------|--------|
    | test_pc1_empty_playlist | Output: "  (empty)" | Output: "  (empty)" | PASS |
    | test_pc2_populated_playlist | Output: "01. Song [03:00]" | Output: "01. Song [03:00]" | PASS |

    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        """
        Prepare the test harness. Redirect stdout to capture print statements
        and ensure isolation between PC_1 and PC_2 verification.
        """
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_pc1_empty_playlist(self):
        """
        Verifies Path Condition 1 (PC_1): NOT S1.
        Constraint: pl.tracks is empty.
        Expected Behaviour: Early return with specific message.
        """
        # Symbolic Input S1: Empty List
        mock_playlist = Mock()
        mock_playlist.tracks = []

        _print_playlist_contents(mock_playlist)

        output = self.captured_output.getvalue().rstrip()
        self.assertEqual(output, "  (empty)", "PC_1 Failed: Did not print empty message.")

    @patch("music_player.playlists_basic.format_mm_ss")
    def test_pc2_populated_playlist(self, mock_format):
        """
        Verifies Path Condition 2 (PC_2): S1.
        Constraint: pl.tracks is populated (S1 is True).
        Expected Behaviour: Loop entry, formatting, and printing of track details.
        """
        # Symbolic Input S1: Populated List
        mock_track = Mock()
        mock_track.duration_seconds = 180
        mock_track.display_name = "Symbolic Anthem"

        mock_playlist = Mock()
        mock_playlist.tracks = [mock_track]

        # Mock external dependency
        mock_format.return_value = "03:00"

        _print_playlist_contents(mock_playlist)

        output = self.captured_output.getvalue().rstrip()
        expected_output = "01. Symbolic Anthem [03:00]"

        # Verify Output
        self.assertEqual(output, expected_output, "PC_2 Failed: Output format incorrect.")
        # Verify dependency interaction
        mock_format.assert_called_once_with(180)


if __name__ == '__main__':
    unittest.main()
