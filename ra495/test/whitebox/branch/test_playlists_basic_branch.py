import unittest
from unittest.mock import MagicMock
from music_player import playlists_basic
from music_player.player_state import PlayerState
from music_player.playlist_model import Playlist
from music_player.library import Track
from pathlib import Path


class TestPlaylistsBasicBranch(unittest.TestCase):
    """
    White-Box Branch Test for playlists_basic.py.
    Testing Tool: Python unittest
    Test Technique: Branch Testing (White-Box)
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        self.pl = Playlist("Mix")
        self.state.playlists = [self.pl]

    def test_resolve_branches(self):
        """
        Branches:
         - Selector is digit - Valid + Invalid Index
         - Selector is string - Name Match + Mismatch
        Expected Result:
         - Returns Playlist object for valid inputs.
         - Returns None for invalid inputs.
        Actual Result:
            [pl] Playlist index out of range.
            [pl] Playlist 'other' not found.
        """
        # Valid Index
        res = playlists_basic._resolve_playlist(self.state, "1")
        self.assertEqual(res, self.pl)
        # Invalid Index
        res = playlists_basic._resolve_playlist(self.state, "5")
        self.assertIsNone(res)
        # Name Match
        res = playlists_basic._resolve_playlist(self.state, "mix")
        self.assertEqual(res, self.pl)
        # Name Mismatch
        res = playlists_basic._resolve_playlist(self.state, "other")
        self.assertIsNone(res)