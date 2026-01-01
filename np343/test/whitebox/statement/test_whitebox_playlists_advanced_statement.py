import unittest
from unittest.mock import MagicMock, patch
from music_player import playlists_advanced
from music_player.player_state import PlayerState

class TestPlaylistsAdvancedStatement(unittest.TestCase):
    """
    White-Box Statement Coverage for playlists_advanced.py.
    Targets: Missing error blocks in _get_playlist and copy/merge validations.
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())
        # Populate playlists to pass initial availability checks
        self.pl1 = MagicMock()
        self.pl1.name = "One"
        self.state.playlists = [self.pl1]