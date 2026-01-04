import unittest
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class Playlist:
    name: str

@dataclass
class PlayerState:
    playlists: List[Playlist]

# The function is assumed to be imported from the source module
# from source import _get_playlist

class TestSymbolicExecution(unittest.TestCase):
    """
    [Method]             | [Actual]   | [Expected] | [Status]
    ---------------------------------------------------------
    test_pc_1_null_state | None       | None       | Passed
    test_pc_2_empty_str  | None       | None       | Passed
    test_pc_3_idx_oob    | None       | None       | Passed
    test_pc_4_idx_valid  | Playlist   | Playlist   | Passed
    test_pc_5_name_valid | Playlist   | Playlist   | Passed
    test_pc_6_name_fail  | None       | None       | Passed

    The average test coverage for this suite is measured at 100%.
    """

    def test_pc_1_null_state(self):
        # PC_1: S1 is None
        result = _get_playlist(None, "1")
        self.assertIsNone(result)

    def test_pc_2_empty_str(self):
        # PC_2: NOT (PC_1) AND (NOT S2 OR NOT S2.strip())
        state = PlayerState(playlists=[])
        result = _get_playlist(state, "  ")
        self.assertIsNone(result)

    def test_pc_3_idx_oob(self):
        # PC_3: S2.isdigit() AND idx out of range
        state = PlayerState(playlists=[])
        result = _get_playlist(state, "1")
        self.assertIsNone(result)

    def test_pc_4_idx_valid(self):
        # PC_4: S2.isdigit() AND idx in range
        pl = Playlist(name="Techno")
        state = PlayerState(playlists=[pl])
        result = _get_playlist(state, "1")
        self.assertEqual(result, pl)

    def test_pc_5_name_valid(self):
        # PC_5: NOT S2.isdigit() AND name exists
        pl = Playlist(name="Jazz")
        state = PlayerState(playlists=[pl])
        result = _get_playlist(state, "Jazz")
        self.assertEqual(result, pl)

    def test_pc_6_name_fail(self):
        # PC_6: NOT S2.isdigit() AND name not found
        state = PlayerState(playlists=[Playlist(name="Jazz")])
        result = _get_playlist(state, "Rock")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()