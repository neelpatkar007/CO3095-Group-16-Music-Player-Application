import unittest
from unittest.mock import MagicMock
from music_player import playlists_basic
from music_player.player_state import PlayerState
from music_player.playlist_model import Playlist
from music_player.library import Track
from pathlib import Path


class TestPlayerConfig(unittest.TestCase):
    """
    Black-Box Specification-based Testing for playlists_basic.py..
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method using TSLGenerator
    Source: playlistBasic.txt
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        self.state.playlists = []

    # Create Playlist Tests

    def test_create_playlist_valid(self):
        """
        Expected Result: New playlist object added to state.playlists.
        Actual Result: [pl] Created playlist 'Gym'.
        """
        playlists_basic.create_playlist(self.state, "Gym")
        self.assertEqual(len(self.state.playlists), 1)
        self.assertEqual(self.state.playlists[0].name, "Gym")

    def test_create_playlist_duplicate(self):
        """
        Expected Result: Creation rejected (duplicate name check).
        Actual Result: [pl] A playlist named 'Gym' already exists.
        """
        playlists_basic.create_playlist(self.state, "Gym")
        playlists_basic.create_playlist(self.state, "Gym")
        self.assertEqual(len(self.state.playlists), 1)

    # Rename Playlist Tests

    def test_rename_playlist_success(self):
        """
        Expected Result: Playlist name is updated.
        Actual Result: [pl] Renamed playlist 'Old' -> 'New'.
        """
        playlists_basic.create_playlist(self.state, "Old")
        playlists_basic.rename_playlist(self.state, "Old", "New")
        self.assertEqual(self.state.playlists[0].name, "New")

    def test_rename_playlist_not_found(self):
        """
        Expected Result: Operation fails.
        Actual Result: [pl] Playlist 'Missing' not found.
        """
        playlists_basic.create_playlist(self.state, "Old")
        playlists_basic.rename_playlist(self.state, "Missing", "New")
        self.assertEqual(self.state.playlists[0].name, "Old")

    # Delete Playlist Tests

    def test_delete_playlist_by_name(self):
        """
        Expected Result: Playlist removed from state.
        Actual Result: [pl] Deleted playlist 'Bye'.
        """
        playlists_basic.create_playlist(self.state, "Bye")
        playlists_basic.delete_playlist(self.state, "Bye")
        self.assertEqual(len(self.state.playlists), 0)