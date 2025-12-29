import unittest
from unittest.mock import MagicMock, patch
from music_player import playlists_basic
from music_player.player_state import PlayerState
from music_player.playlist_model import Playlist
from music_player.library import Track
from pathlib import Path


class TestPlaylistsBasicStatement(unittest.TestCase):
    """
    White-Box Statement Testing for playlists_basic.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Statement Testing (White-Box)
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        self.state.playlists = []
        self.pl = Playlist("Mix")

    def test_ensure_and_resolve_errors(self):
        """
        Expected Result: Helper functions handle invalid inputs without crashing.
        Actual Result:
            [pl] Error: State is None.
            [pl] Error: State is None.
            [pl] Error: State is None.
            [pl] Missing playlist name or number.
            [pl] Error: State is None.
            [pl] Playlist index out of range.
            [pl] Playlist 'Missing' not found.
        """
        # _ensure_playlists errors
        playlists_basic._ensure_playlists(None)

        # _resolve_playlist errors
        playlists_basic._resolve_playlist(None, "1")
        playlists_basic._resolve_playlist(self.state, 123)

        self.state.playlists = "NotList"  # Corrupt playlists
        playlists_basic._resolve_playlist(self.state, "1")

        self.state.playlists = []
        playlists_basic._resolve_playlist(self.state, "99")
        playlists_basic._resolve_playlist(self.state, "Missing")