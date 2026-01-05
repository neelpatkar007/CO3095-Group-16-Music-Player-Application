import unittest
from dataclasses import dataclass


@dataclass
class MockPlaylist:

    name: str
    num_tracks: int
    total_duration_mm_ss: str

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

    def setUp(self):
        self.s3_name = "SymbolicHits"
        self.s4_tracks = 12
        self.s5_duration = "42:00"
        self.playlist = MockPlaylist(self.s3_name, self.s4_tracks, self.s5_duration)

    def test_pc1_int_active(self):
        s1 = 1
        s2 = True

        result = self.playlist.summary_line(index=s1, active=s2)

        expected_marker = "*"
        expected_idx = "01"

        self.assertIn(expected_marker, result, "PC_1 failed: Active marker '*' missing.")
        self.assertIn(expected_idx, result, "PC_1 failed: Index formatting incorrect.")

    def test_pc2_int_inactive(self):
        s1 = 5
        s2 = False

        result = self.playlist.summary_line(index=s1, active=s2)
        self.assertTrue(result.startswith("  05"),
                        f"PC_2 failed: Output '{result}' does not match expected start '  05'.")

    def test_pc3_none_active(self):
        s1 = None
        s2 = True

        result = self.playlist.summary_line(index=s1, active=s2)

        expected_marker = "*"
        expected_idx = "--"

        self.assertIn(expected_marker, result, "PC_3 failed: Active marker '*' missing.")
        self.assertIn(expected_idx, result, "PC_3 failed: Default index '--' missing.")

    def test_pc4_none_inactive(self):
        s1 = None
        s2 = False

        result = self.playlist.summary_line(index=s1, active=s2)
        self.assertTrue(result.startswith("  --"),
                        f"PC_4 failed: Output '{result}' does not match expected start '  --'.")


if __name__ == '__main__':
    unittest.main()