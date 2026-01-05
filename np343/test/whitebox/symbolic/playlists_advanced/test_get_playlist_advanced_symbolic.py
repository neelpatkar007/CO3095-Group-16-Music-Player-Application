import unittest
from unittest.mock import MagicMock
from music_player.playlists_advanced import _get_playlist


class TestSymbolicExecution(unittest.TestCase):
    def test_pc_1_null_state(self):
        result = _get_playlist(None, "1")
        self.assertIsNone(result)

    def test_pc_2_empty_str(self):
        state = MagicMock(playlists=[])
        result = _get_playlist(state, "  ")
        self.assertIsNone(result)

    def test_pc_3_idx_oob(self):
        state = MagicMock(playlists=[])
        result = _get_playlist(state, "1")
        self.assertIsNone(result)

    def test_pc_4_idx_valid(self):
        pl = MagicMock()
        pl.name = "Techno"
        state = MagicMock(playlists=[pl])
        result = _get_playlist(state, "1")
        self.assertEqual(result, pl)

    def test_pc_5_name_valid(self):
        pl = MagicMock()
        pl.name = "Jazz"
        state = MagicMock(playlists=[pl])
        result = _get_playlist(state, "Jazz")
        self.assertEqual(result, pl)

    def test_pc_6_name_fail(self):
        pl = MagicMock()
        pl.name = "Jazz"
        state = MagicMock(playlists=[pl])
        result = _get_playlist(state, "Rock")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()