# python
import unittest
from unittest.mock import MagicMock, patch
from music_player.playlists_basic import delete_playlist


class TestSymbolicExecution(unittest.TestCase):
    """
    White-box testing suite based on Symbolic Execution Analysis (FILE 1).
    Tests strictly map to Path Conditions (PC_1 to PC_6).
    """

    def setUp(self):
        """Set up the mock state and playlist objects for each test."""
        self.state = MagicMock()
        self.playlist_mock = MagicMock()
        self.playlist_mock.name = "TestPlaylist"

        # Default behaviour for _ensure_playlists (pass-through)
        self.ensure_patcher = patch('music_player.playlists_basic._ensure_playlists')
        self.mock_ensure = self.ensure_patcher.start()

        # Patcher for _resolve_playlist
        self.resolve_patcher = patch('music_player.playlists_basic._resolve_playlist')
        self.mock_resolve = self.resolve_patcher.start()

    def tearDown(self):
        self.ensure_patcher.stop()
        self.resolve_patcher.stop()

    def test_pc1_early_return(self):
        """
        PC_1: S1 IS None.
        Expectation: Function returns immediately, no deletion occurs.
        """
        # S1 = None
        self.mock_resolve.return_value = None

        delete_playlist(self.state, "selector")

        # Assertions
        self.mock_resolve.assert_called_once()
        # Verify no deletion happened on state.playlists
        self.state.playlists.index.assert_not_called()

    def test_pc2_no_active_index(self):
        """
        PC_2: S1 IS NOT None AND S2 IS None.
        Expectation: Playlist deleted, active index remains None.
        """
        # S1 = Object
        self.mock_resolve.return_value = self.playlist_mock
        # S2 = None
        self.state.active_playlist_index = None
        # Setup lists
        self.state.playlists = [self.playlist_mock]

        delete_playlist(self.state, "selector")

        # Assertions
        self.assertFalse(self.playlist_mock in self.state.playlists)
        self.assertIsNone(self.state.active_playlist_index)

    def test_pc3_decrement_index(self):
        """
        PC_3: S1 IS NOT None AND S2 IS NOT None AND S3 < S2.
        Expectation: Index decrements (1 -> 0).
        """
        # S1 = Object
        other_pl = MagicMock()
        self.mock_resolve.return_value = self.playlist_mock

        # Setup List: [Target, Other]
        # Target is at index 0 (S3=0)
        self.state.playlists = [self.playlist_mock, other_pl]

        # S2 = 1 (Active index points to 'other_pl')
        self.state.active_playlist_index = 1

        delete_playlist(self.state, "selector")

        # Assertions
        self.assertEqual(len(self.state.playlists), 1)
        self.assertEqual(self.state.active_playlist_index, 0)

    def test_pc4_idx_greater(self):
        """
        PC_4: S1 IS NOT None AND S2 IS NOT None AND NOT (S3 < S2) AND NOT (S3 == S2).
        Implies S3 > S2.
        Expectation: Index remains unchanged.
        """
        # S1 = Object
        other_pl = MagicMock()
        self.mock_resolve.return_value = self.playlist_mock

        # Setup List: [Other, Target]
        # Target is at index 1 (S3=1)
        self.state.playlists = [other_pl, self.playlist_mock]

        # S2 = 0 (Active index points to 'other_pl')
        self.state.active_playlist_index = 0

        delete_playlist(self.state, "selector")

        # Assertions
        self.assertEqual(len(self.state.playlists), 1)
        self.assertEqual(self.state.active_playlist_index, 0)

    def test_pc5_delete_active_empty(self):
        """
        PC_5: S1 IS NOT None, S2 IS NOT None, S3 == S2, S4 IS Empty.
        Expectation: Active index becomes None.
        """
        # S1 = Object
        self.mock_resolve.return_value = self.playlist_mock

        # Setup List: [Target]
        # S3 = 0
        self.state.playlists = [self.playlist_mock]

        # S2 = 0
        self.state.active_playlist_index = 0

        delete_playlist(self.state, "selector")

        # Assertions
        self.assertEqual(len(self.state.playlists), 0)  # S4 is empty
        self.assertIsNone(self.state.active_playlist_index)

    def test_pc6_delete_active_rem(self):
        """
        PC_6: S1 IS NOT None, S2 IS NOT None, S3 == S2, S4 IS NOT Empty.
        Expectation: Active index resets to 0.
        """
        # S1 = Object
        other_pl = MagicMock()
        self.mock_resolve.return_value = self.playlist_mock

        # Setup List: [Target, Other]
        # S3 = 0
        self.state.playlists = [self.playlist_mock, other_pl]

        # S2 = 0
        self.state.active_playlist_index = 0

        delete_playlist(self.state, "selector")

        # Assertions
        self.assertEqual(len(self.state.playlists), 1)  # S4 is not empty
        self.assertEqual(self.state.active_playlist_index, 0)
