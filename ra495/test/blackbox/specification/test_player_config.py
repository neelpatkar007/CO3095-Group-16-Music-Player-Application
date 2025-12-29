import unittest
import json
from unittest.mock import MagicMock, patch, mock_open
from music_player import player_config, playlists_basic
from music_player.player_state import PlayerState
from music_player.library import Track
from pathlib import Path


class TestPlayerConfig(unittest.TestCase):
    """
    Black-Box Specification-based Testing for player_config.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Category Partition Method using TSLGenerator
    Source: playerConfig.txt
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        # Setup dummy library for testing tags/stats
        self.track1 = Track(Path("a.mp3"), "Song A", "Artist A", 100)
        self.track2 = Track(Path("b.mp3"), "Song B", "Artist B", 200)
        self.state.library_tracks = [self.track1, self.track2]

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