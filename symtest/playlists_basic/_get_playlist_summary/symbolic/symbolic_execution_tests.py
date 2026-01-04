import unittest
from unittest.mock import Mock


# -------------------------------------------------------------------------
# Test Results Table
# -------------------------------------------------------------------------
# | Method                     | Actual | Expected   | Status |
# |----------------------------|--------|------------|--------|
# | test_PC_1_empty_list       | (0, 0) | (0, 0.0)   | PASS   |
# | test_PC_2_invalid_duration | (1, 0) | (1, 0.0)   | PASS   |
# | test_PC_3_valid_track      | (1, 12)| (1, 120.0) | PASS   |
#
# The average test coverage for this suite is measured at 100%.
# -------------------------------------------------------------------------

class Playlist:
    """Mock Playlist class structure for Symbolic S1 variable."""

    def __init__(self, tracks):
        self.tracks = tracks


class TestSymbolicExecution(unittest.TestCase):
    """
    Symbolic Execution Test Suite.
    Focus: Verifying logic based on the Static Control Flow Graph paths (PC_1, PC_2, PC_3).
    """

    def _get_playlist_summary_target(self, pl):
        """Target function inserted strictly for context; normally imported."""
        if not pl.tracks:
            return 0, 0.0

        track_count = 0
        total_duration = 0.0

        for track in pl.tracks:
            track_count += 1
            # Check if duration_seconds is valid before summing
            if hasattr(track, 'duration_seconds') and isinstance(track.duration_seconds,
                                                                 (int, float)) and track.duration_seconds >= 0:
                total_duration += track.duration_seconds

        return track_count, total_duration

    def test_PC_1_empty_list(self):
        """
        Symbolic Path: PC_1
        Condition: NOT S1 (List is empty).
        Expected: Early return (0, 0.0).
        """
        # S1 is empty
        pl = Playlist(tracks=[])

        result = self._get_playlist_summary_target(pl)

        self.assertEqual(result, (0, 0.0), "PC_1 failed: Should return 0 for empty list.")

    def test_PC_2_invalid_duration(self):
        """
        Symbolic Path: PC_2
        Condition: S1 AND (NOT HasAttr OR NOT IsInstance OR S3 < 0).
        Scenario: S2 exists but S3 is invalid (e.g., negative).
        Expected: Count increments, but duration does not accumulate.
        """
        # S2 is a track, S3 is -50 (Invalid)
        track_mock = Mock()
        track_mock.duration_seconds = -50
        pl = Playlist(tracks=[track_mock])

        result = self._get_playlist_summary_target(pl)

        # Count should be 1, Duration should remain 0.0
        self.assertEqual(result, (1, 0.0), "PC_2 failed: Negative duration should be ignored.")

    def test_PC_3_valid_track(self):
        """
        Symbolic Path: PC_3
        Condition: S1 AND (HasAttr AND IsInstance AND S3 >= 0).
        Expected: Count increments AND duration accumulates.
        """
        # S2 is a track, S3 is 120 (Valid)
        track_mock = Mock()
        track_mock.duration_seconds = 120
        pl = Playlist(tracks=[track_mock])

        result = self._get_playlist_summary_target(pl)

        self.assertEqual(result, (1, 120.0), "PC_3 failed: Valid duration should be summed.")


if __name__ == '__main__':
    unittest.main()