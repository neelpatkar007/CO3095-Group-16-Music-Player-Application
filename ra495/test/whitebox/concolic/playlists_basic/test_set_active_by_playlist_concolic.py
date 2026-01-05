import unittest
from unittest.mock import MagicMock
from music_player.playlists_basic import _set_active_by_playlist


class TestConcolicExecution(unittest.TestCase):
    def setUp(self):
        self.S1_state = MagicMock()
        self.S2_playlist = MagicMock()
        self.S1_state.active_playlist_index = None

    def test_iteration_1_flip(self):
        self.S1_state.playlists = []

        _set_active_by_playlist(self.S1_state, self.S2_playlist)

        self.assertIsNone(
            self.S1_state.active_playlist_index,
            "Concolic Iteration 1 Failed: Should have followed PC_1 (Exception path)."
        )

    def test_iteration_2_derived(self):
        self.S1_state.playlists = [self.S2_playlist, MagicMock()]  # S2 at index 0

        _set_active_by_playlist(self.S1_state, self.S2_playlist)

        self.assertEqual(
            self.S1_state.active_playlist_index,
            0,
            "Concolic Iteration 2 Failed: Should have followed PC_2 (Success path)."
        )


if __name__ == '__main__':
    unittest.main()