# python
import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import delete_playlist


class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()
        self.playlist_mock = MagicMock()
        self.playlist_mock.name = "TestPlaylist"

        self.ensure_patcher = patch('music_player.playlists_basic._ensure_playlists')
        self.mock_ensure = self.ensure_patcher.start()

        self.resolve_patcher = patch('music_player.playlists_basic._resolve_playlist')
        self.mock_resolve = self.resolve_patcher.start()

    def tearDown(self):
        self.ensure_patcher.stop()
        self.resolve_patcher.stop()

    def test_pc1_early_return(self):
        self.mock_resolve.return_value = None

        delete_playlist(self.state, "selector")

        self.mock_resolve.assert_called_once()
        self.state.playlists.index.assert_not_called()

    def test_pc2_no_active_index(self):
        self.mock_resolve.return_value = self.playlist_mock
        self.state.active_playlist_index = None
        self.state.playlists = [self.playlist_mock]

        delete_playlist(self.state, "selector")

        self.assertFalse(self.playlist_mock in self.state.playlists)
        self.assertIsNone(self.state.active_playlist_index)

    def test_pc3_decrement_index(self):
        other_pl = MagicMock()
        self.mock_resolve.return_value = self.playlist_mock

        self.state.playlists = [self.playlist_mock, other_pl]

        self.state.active_playlist_index = 1

        delete_playlist(self.state, "selector")

        self.assertEqual(len(self.state.playlists), 1)
        self.assertEqual(self.state.active_playlist_index, 0)

    def test_pc4_idx_greater(self):
        other_pl = MagicMock()
        self.mock_resolve.return_value = self.playlist_mock

        self.state.playlists = [other_pl, self.playlist_mock]

        self.state.active_playlist_index = 0

        delete_playlist(self.state, "selector")

        self.assertEqual(len(self.state.playlists), 1)
        self.assertEqual(self.state.active_playlist_index, 0)

    def test_pc5_delete_active_empty(self):

        self.mock_resolve.return_value = self.playlist_mock

        self.state.playlists = [self.playlist_mock]


        self.state.active_playlist_index = 0

        delete_playlist(self.state, "selector")

        self.assertEqual(len(self.state.playlists), 0)  # S4 is empty
        self.assertIsNone(self.state.active_playlist_index)

    def test_pc6_delete_active_rem(self):

        other_pl = MagicMock()
        self.mock_resolve.return_value = self.playlist_mock

        self.state.playlists = [self.playlist_mock, other_pl]


        self.state.active_playlist_index = 0

        delete_playlist(self.state, "selector")


        self.assertEqual(len(self.state.playlists), 1)  # S4 is not empty
        self.assertEqual(self.state.active_playlist_index, 0)
