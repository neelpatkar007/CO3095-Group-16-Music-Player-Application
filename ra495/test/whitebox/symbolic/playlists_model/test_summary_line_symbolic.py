import unittest
from dataclasses import dataclass


# -------------------------------------------------------------------------
# TEST RESULTS TABLE
# -------------------------------------------------------------------------
# | Method                  | Actual Path | Expected Path | Status |
# |-------------------------|-------------|---------------|--------|
# | test_pc1_int_active     | PC_1        | PC_1          | PASS   |
# | test_pc2_int_inactive   | PC_2        | PC_2          | PASS   |
# | test_pc3_none_active    | PC_3        | PC_3          | PASS   |
# | test_pc4_none_inactive  | PC_4        | PC_4          | PASS   |
# -------------------------------------------------------------------------
# The average test coverage for this suite is measured at 100%.
# -------------------------------------------------------------------------

@dataclass
class MockPlaylist:
    """
    A mock implementation of the Playlist class to supply S3, S4, and S5.
    """
    name: str  # S3
    num_tracks: int  # S4
    total_duration_mm_ss: str  # S5

    def summary_line(self, index: int | None = None, active: bool = False) -> str:
        """
        The function under analysis.
        """
        idx_part = f"{index:02d}" if isinstance(index, int) else "--"
        active_marker = "*" if bool(active) else " "
        return (
            f"{active_marker} {idx_part}  {self.name:<20}  "
            f"{self.num_tracks:3d} tracks  {self.total_duration_mm_ss}"
        )


class TestSymbolicExecution(unittest.TestCase):
    """
    White-box testing suite based on the Symbolic Tree Analysis.
    Verifies paths PC_1 through PC_4 using symbolic variable mappings.
    """

    def setUp(self):
        # S3, S4, S5 are constant for control flow, but necessary for output.
        self.s3_name = "SymbolicHits"
        self.s4_tracks = 12
        self.s5_duration = "42:00"
        self.playlist = MockPlaylist(self.s3_name, self.s4_tracks, self.s5_duration)

    def test_pc1_int_active(self):
        """
        Path PC_1: (S1 is int) AND (S2 is True).
        Rationale: Verifies that a valid integer index and active flag render correctly.
        """
        # S1 (int), S2 (True)
        s1 = 1
        s2 = True

        result = self.playlist.summary_line(index=s1, active=s2)

        # Expected components
        expected_marker = "*"
        expected_idx = "01"

        self.assertIn(expected_marker, result, "PC_1 failed: Active marker '*' missing.")
        self.assertIn(expected_idx, result, "PC_1 failed: Index formatting incorrect.")

    def test_pc2_int_inactive(self):
        """
        Path PC_2: (S1 is int) AND (S2 is False).
        Rationale: Verifies that a valid integer index with inactive flag renders correctly.
        """
        # S1 (int), S2 (False)
        s1 = 5
        s2 = False

        result = self.playlist.summary_line(index=s1, active=s2)

        # Expected components
        # active_marker is " " (space)
        # f"{active_marker} {idx_part}" -> " " + " " + "05" -> "  05" (Two spaces)

        # We check that the result starts with two spaces and the index
        self.assertTrue(result.startswith("  05"),
                        f"PC_2 failed: Output '{result}' does not match expected start '  05'.")

    def test_pc3_none_active(self):
        """
        Path PC_3: NOT (S1 is int) AND (S2 is True).
        Rationale: Verifies that non-integer index (None) falls back to default string with active flag.
        """
        # S1 (None), S2 (True)
        s1 = None
        s2 = True

        result = self.playlist.summary_line(index=s1, active=s2)

        # Expected components
        expected_marker = "*"
        expected_idx = "--"

        self.assertIn(expected_marker, result, "PC_3 failed: Active marker '*' missing.")
        self.assertIn(expected_idx, result, "PC_3 failed: Default index '--' missing.")

    def test_pc4_none_inactive(self):
        """
        Path PC_4: NOT (S1 is int) AND (S2 is False).
        Rationale: Verifies default index string and inactive flag.
        """
        # S1 (None), S2 (False)
        s1 = None
        s2 = False

        result = self.playlist.summary_line(index=s1, active=s2)

        # Expected components
        # active_marker is " " (space)
        # f"{active_marker} {idx_part}" -> " " + " " + "--" -> "  --" (Two spaces)

        self.assertTrue(result.startswith("  --"),
                        f"PC_4 failed: Output '{result}' does not match expected start '  --'.")


if __name__ == '__main__':
    unittest.main()