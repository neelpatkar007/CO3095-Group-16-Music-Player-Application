import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import delete_playlist

class TestConcolicGeneration(unittest.TestCase):

    def setUp(self):
        self.state = MagicMock()
        self.playlist_mock = MagicMock()
        self.playlist_mock.name = "ConcolicPL"

        self.ensure_patcher = patch('music_player.playlists_basic._ensure_playlists')
        self.mock_ensure = self.ensure_patcher.start()

        self.resolve_patcher = patch('music_player.playlists_basic._resolve_playlist')
        self.mock_resolve = self.resolve_patcher.start()

    def tearDown(self):
        self.ensure_patcher.stop()
        self.resolve_patcher.stop()

    def test_iteration_1_base(self):
        self.mock_resolve.return_value = None

        delete_playlist(self.state, "sel")

        self.mock_resolve.assert_called()
        self.state.playlists.index.assert_not_called()

    def test_iteration_2_flip_null(self):
        self.mock_resolve.return_value = self.playlist_mock
        self.state.active_playlist_index = None  # S2
        self.state.playlists = [self.playlist_mock]

        delete_playlist(self.state, "sel")

        self.assertIsNone(self.state.active_playlist_index)

    def test_iteration_3_flip_less(self):
        other = MagicMock()
        self.mock_resolve.return_value = self.playlist_mock
        self.state.playlists = [self.playlist_mock, other]
        self.state.active_playlist_index = 1  # S2

        delete_playlist(self.state, "sel")

        self.assertEqual(self.state.active_playlist_index, 0)

    def test_iteration_4_flip_gtr(self):
        other = MagicMock()
        self.mock_resolve.return_value = self.playlist_mock
        self.state.playlists = [other, self.playlist_mock]
        self.state.active_playlist_index = 0  # S2

        delete_playlist(self.state, "sel")

        self.assertEqual(self.state.active_playlist_index, 0)

    def test_iteration_5_flip_empty(self):
        self.mock_resolve.return_value = self.playlist_mock
        self.state.playlists = [self.playlist_mock]
        self.state.active_playlist_index = 0  # S2

        delete_playlist(self.state, "sel")

        self.assertIsNone(self.state.active_playlist_index)

    def test_iteration_6_flip_rem(self):
        other = MagicMock()
        self.mock_resolve.return_value = self.playlist_mock
        self.state.playlists = [self.playlist_mock, other]
        self.state.active_playlist_index = 0  # S2

        delete_playlist(self.state, "sel")

        self.assertEqual(self.state.active_playlist_index, 0)
