import unittest
from dataclasses import dataclass

@dataclass
class MockPlaylist:
    name: str
    num_tracks: int
    total_duration_mm_ss: str

    def summary_line(self, index: int | None = None, active: bool = False) -> str:
        idx_part = f"{index:02d}" if isinstance(index, int) else "--"
        active_marker = "*" if bool(active) else " "
        return (
            f"{active_marker} {idx_part}  {self.name:<20}  "
            f"{self.num_tracks:3d} tracks  {self.total_duration_mm_ss}"
        )


class TestConcolicExecution(unittest.TestCase):

    def setUp(self):
        self.playlist = MockPlaylist("ConcolicTest", 99, "59:59")

    def test_iteration_1_base_case(self):
        s1 = None
        s2 = False
        result = self.playlist.summary_line(index=s1, active=s2)
        self.assertIn("--", result)
        self.assertTrue(result.startswith("  --"), f"Iteration 1 failed: Expected start '  --', got '{result[:4]}'")

    def test_iteration_2_flip_active(self):
        s1 = None
        s2 = True
        result = self.playlist.summary_line(index=s1, active=s2)

        self.assertIn("*", result)
        self.assertIn("--", result)

    def test_iteration_3_flip_type_check(self):
        s1 = 1
        s2 = True
        result = self.playlist.summary_line(index=s1, active=s2)

        # Validation
        self.assertIn("*", result)
        self.assertIn("01", result)

    def test_iteration_4_flip_active_again(self):
        s1 = 1
        s2 = False
        result = self.playlist.summary_line(index=s1, active=s2)
        self.assertIn("01", result)
        self.assertTrue(result.startswith("  01"), f"Iteration 4 failed: Expected start '  01', got '{result[:4]}'")


if __name__ == '__main__':
    unittest.main()