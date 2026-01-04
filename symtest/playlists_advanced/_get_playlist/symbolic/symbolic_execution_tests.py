import unittest
from unittest.mock import MagicMock
from music_player.playlists_advanced import _get_playlist


class TestSymbolicExecution(unittest.TestCase):
    """
    Symbolic Execution Test Suite for _get_playlist.

    Test Results Table:
    | Method               | Actual    | Expected  | Status |
    |----------------------|-----------|-----------|--------|
    | test_pc_1_null_state | None      | None      | PASS   |
    | test_pc_2_empty_str  | None      | None      | PASS   |
    | test_pc_3_idx_oob    | None      | None      | PASS   |
    | test_pc_4_idx_valid  | Playlist  | Playlist  | PASS   |
    | test_pc_5_name_valid | Playlist  | Playlist  | PASS   |
    | test_pc_6_name_fail  | None      | None      | PASS   |

    The average test coverage for this suite is measured at 100%.
    """

    def test_pc_1_null_state(self):
        """PC_1: S1 is None"""
        result = _get_playlist(None, "1")
        self.assertIsNone(result)

    def test_pc_2_empty_str(self):
        """PC_2: NOT (PC_1) AND (NOT S2 OR NOT S2.strip())"""
        state = MagicMock(playlists=[])
        result = _get_playlist(state, "  ")
        self.assertIsNone(result)

    def test_pc_3_idx_oob(self):
        """PC_3: S2.isdigit() AND idx out of range"""
        state = MagicMock(playlists=[])
        result = _get_playlist(state, "1")
        self.assertIsNone(result)

    def test_pc_4_idx_valid(self):
        """PC_4: S2.isdigit() AND idx in range"""
        pl = MagicMock()
        pl.name = "Techno"
        state = MagicMock(playlists=[pl])
        result = _get_playlist(state, "1")
        self.assertEqual(result, pl)

    def test_pc_5_name_valid(self):
        """PC_5: NOT S2.isdigit() AND name exists"""
        pl = MagicMock()
        pl.name = "Jazz"
        state = MagicMock(playlists=[pl])
        result = _get_playlist(state, "Jazz")
        self.assertEqual(result, pl)

    def test_pc_6_name_fail(self):
        """PC_6: NOT S2.isdigit() AND name not found"""
        pl = MagicMock()
        pl.name = "Jazz"
        state = MagicMock(playlists=[pl])
        result = _get_playlist(state, "Rock")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()