import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import _set_active_by_playlist

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.S1_state = MagicMock()
        self.S2_playlist = MagicMock()
        self.S1_state.active_playlist_index = None

    def test_pc1_exception(self):

        self.S1_state.playlists = []

        _set_active_by_playlist(self.S1_state, self.S2_playlist)

        self.assertIsNone(
            self.S1_state.active_playlist_index,
            "PC_1 Failure: State should not be updated when ValueError is caught."
        )

    def test_pc2_success(self):
        self.S1_state.playlists = [self.S2_playlist]

        _set_active_by_playlist(self.S1_state, self.S2_playlist)

        self.assertEqual(
            self.S1_state.active_playlist_index,
            0,
            "PC_2 Failure: State should be updated to the correct index."
        )


if __name__ == '__main__':
    unittest.main()