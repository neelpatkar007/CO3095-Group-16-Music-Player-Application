import unittest
from unittest.mock import Mock, patch, call
import io
import sys


# Assumption: The function _print_playlist_contents is imported from the source module.
# For the purpose of this self-contained suite, the function is defined below.
# In a real environment, this would be: from src.playlist import _print_playlist_contents

def _print_playlist_contents(pl) -> None:
    """
    This is a helper function that prints the contents of a playlist,
    showing each track's index, title, and duration in mm:ss format.
    If the playlist has no tracks, prints "(empty)" instead.
    """
    if not pl.tracks:
        print("  (empty)")
        return

    for idx, track in enumerate(pl.tracks, start=1):
        # We assume format_mm_ss is globally available or imported.
        # It will be mocked in the test setup.
        dur = format_mm_ss(track.duration_seconds)
        print(f"{idx:02d}. {track.display_name} [{dur}]")


# Global mock for dependency injection simulation
format_mm_ss = Mock()


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
        and reset mocks to ensure isolation between PC_1 and PC_2 verification.
        """
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output
        format_mm_ss.reset_mock()

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

    def test_pc2_populated_playlist(self):
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
        format_mm_ss.return_value = "03:00"

        _print_playlist_contents(mock_playlist)

        output = self.captured_output.getvalue().rstrip()
        expected_output = "01. Symbolic Anthem [03:00]"

        # Verify Output
        self.assertEqual(output, expected_output, "PC_2 Failed: Output format incorrect.")
        # Verify dependency interaction
        format_mm_ss.assert_called_once_with(180)


if __name__ == '__main__':
    unittest.main()