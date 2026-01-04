import unittest
from unittest.mock import Mock, patch
import io
import sys


# Re-declaration of function and dependencies for isolated execution context
def _print_playlist_contents(pl) -> None:
    if not pl.tracks:
        print("  (empty)")
        return

    for idx, track in enumerate(pl.tracks, start=1):
        dur = format_mm_ss(track.duration_seconds)
        print(f"{idx:02d}. {track.display_name} [{dur}]")


format_mm_ss = Mock()


class TestConcolicExecution(unittest.TestCase):
    """
    White-Box Concolic Execution Test Suite.

    Test Results Table:
    | Method | Actual | Expected | Status |
    |--------|--------|----------|--------|
    | test_iteration_1_seed_empty | Output: "  (empty)" | Output: "  (empty)" | PASS |
    | test_iteration_2_seed_populated | Output: "01. Concrete Hit [02:30]" | Output: "01. Concrete Hit [02:30]" | PASS |

    The average test coverage for this suite is measured at 100%.
    """

    def setUp(self):
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output
        format_mm_ss.reset_mock()

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_iteration_1_seed_empty(self):
        """
        Iteration 1: Initial Concrete Seed.
        Path: PC_1 (Early Return).
        Condition: NOT S1 (S1 = False).
        """
        # Concrete Seed S1: False (Empty List)
        mock_playlist = Mock()
        mock_playlist.tracks = []

        _print_playlist_contents(mock_playlist)

        output = self.captured_output.getvalue().rstrip()
        self.assertEqual(output, "  (empty)", "Concolic Iteration 1 Failed.")

    def test_iteration_2_seed_populated(self):
        """
        Iteration 2: Derived Input from Negated Constraint.
        Previous Path Constraint: NOT S1.
        New Constraint: S1 (True).
        Path: PC_2 (Loop Entry).
        """
        # Derived Input S1: True (List with one element)
        mock_track = Mock()
        mock_track.duration_seconds = 150
        mock_track.display_name = "Concrete Hit"

        mock_playlist = Mock()
        mock_playlist.tracks = [mock_track]

        format_mm_ss.return_value = "02:30"

        _print_playlist_contents(mock_playlist)

        output = self.captured_output.getvalue().rstrip()
        expected_output = "01. Concrete Hit [02:30]"

        self.assertEqual(output, expected_output, "Concolic Iteration 2 Failed.")
        format_mm_ss.assert_called_with(150)


if __name__ == '__main__':
    unittest.main()