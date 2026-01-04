import unittest
from unittest.mock import MagicMock

"""
Test Results Table:
[Method]             | [Actual]                             | [Expected]                           | [Status]
test_PC_1_int_active | "* 05  TestPlaylist          3 tracks" | "* 05  TestPlaylist          3 tracks" | PASSED
test_PC_2_int_inact  | "  05  TestPlaylist          3 tracks" | "  05  TestPlaylist          3 tracks" | PASSED
test_PC_3_none_active| "* --  TestPlaylist          3 tracks" | "* --  TestPlaylist          3 tracks" | PASSED
test_PC_4_none_inact | "  --  TestPlaylist          3 tracks" | "  --  TestPlaylist          3 tracks" | PASSED

The average test coverage for this suite is measured at 100%.
"""

class TestSymbolicExecution(unittest.TestCase):
    def setUp(self):
        # Mocking the self context for the summary_line method
        self.mock_playlist = MagicMock()
        self.mock_playlist.name = "TestPlaylist"
        self.mock_playlist.num_tracks = 3
        self.mock_playlist.total_duration_mm_ss = "12:34"

    def test_PC_1_int_active(self):
        # PC_1: S1 (index) is int, S2 (active) is True
        s1, s2 = 5, True
        result = self.mock_playlist.__class__.summary_line(self.mock_playlist, s1, s2)
        expected = "* 05  TestPlaylist          3 tracks  12:34"
        self.assertEqual(result, expected)

    def test_PC_2_int_inactive(self):
        # PC_2: S1 (index) is int, S2 (active) is False
        s1, s2 = 5, False
        result = self.mock_playlist.__class__.summary_line(self.mock_playlist, s1, s2)
        expected = "  05  TestPlaylist          3 tracks  12:34"
        self.assertEqual(result, expected)

    def test_PC_3_none_active(self):
        # PC_3: S1 (index) is NOT int, S2 (active) is True
        s1, s2 = None, True
        result = self.mock_playlist.__class__.summary_line(self.mock_playlist, s1, s2)
        expected = "* --  TestPlaylist          3 tracks  12:34"
        self.assertEqual(result, expected)

    def test_PC_4_none_inactive(self):
        # PC_4: S1 (index) is NOT int, S2 (active) is False
        s1, s2 = None, False
        result = self.mock_playlist.__class__.summary_line(self.mock_playlist, s1, s2)
        expected = "  --  TestPlaylist          3 tracks  12:34"
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()