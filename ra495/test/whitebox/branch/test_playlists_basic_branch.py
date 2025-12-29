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