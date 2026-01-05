import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path


from music_player.playlists_edit import _get_playlist


class TestConcolicTesting(unittest.TestCase):


    def test_iteration_exploration(self):
        self.assertIsNone(_get_playlist(None, "jazz"), "Failed PC_1")

        state_inst = MagicMock()
        self.assertIsNone(_get_playlist(state_inst, ""), "Failed PC_2")

        with patch('music_player.playlists_edit._ensure_playlists'), \
             patch('music_player.playlists_edit._resolve_playlist', return_value=None):
            self.assertIsNone(_get_playlist(state_inst, "jazz"), "Failed PC_3")

        pl_mock = MagicMock()
        state_inst.playlists = []
        with patch('music_player.playlists_edit._ensure_playlists'), \
             patch('music_player.playlists_edit._resolve_playlist', return_value=pl_mock):
            self.assertIsNone(_get_playlist(state_inst, "jazz"), "Failed PC_4")

        state_inst.playlists = [pl_mock]
        with patch('music_player.playlists_edit._ensure_playlists'), \
             patch('music_player.playlists_edit._resolve_playlist', return_value=pl_mock):
            idx, res = _get_playlist(state_inst, "jazz")
            self.assertEqual(idx, 0)
            self.assertEqual(res, pl_mock)


if __name__ == '__main__':
    unittest.main()