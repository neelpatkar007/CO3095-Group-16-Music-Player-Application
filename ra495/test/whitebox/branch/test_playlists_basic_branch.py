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

    def test_sort_lambda_branches(self):
        """
        Branches:
         - Lambda logic for title, artist, duration sorting
        Expected Result:
         - Missing title sorts as "".
         - Missing artist sorts as "unknown".
         - Missing duration sorts as 0.0.
        Actual Result:
            [pl] Sorted playlist 'Mix' by title.
            [pl] Sorted playlist 'Mix' by artist.
            [pl] Sorted playlist 'Mix' by duration.
        """
        t_good = Track(Path("a"), "B_Good", "B_Art", 100)
        # Broken track with None attributes
        t_bad = Track(Path("b"), "", "", 0)
        t_bad.title = None
        t_bad.artist = None
        t_bad.duration_seconds = None
        self.pl.tracks = [t_good, t_bad]
        # Sort Title
        playlists_basic.sort_playlist(self.state, "Mix", "title")
        self.assertEqual(self.pl.tracks[0], t_bad)
        # Sort Artist
        playlists_basic.sort_playlist(self.state, "Mix", "artist")
        self.assertEqual(self.pl.tracks[0], t_good)
        # Sort Duration
        playlists_basic.sort_playlist(self.state, "Mix", "duration")
        self.assertEqual(self.pl.tracks[0], t_bad)