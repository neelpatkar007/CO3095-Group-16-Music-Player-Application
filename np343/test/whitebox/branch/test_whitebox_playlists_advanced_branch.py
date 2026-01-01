import unittest
from unittest.mock import MagicMock, patch
from music_player import playlists_advanced
from music_player.player_state import PlayerState


class TestPlaylistsAdvancedBranch(unittest.TestCase):
    """
    White-Box Branch Tests for playlists_advanced.py.
    Tools: Python unittest + unittest.mock
    Technique: White-Box Branch Testing
    """

    def setUp(self):
        self.pl1 = MagicMock();
        self.pl1.name = "One"
        self.pl2 = MagicMock();
        self.pl2.name = "Two"
        self.state = PlayerState([], MagicMock())
        self.state.playlists = [self.pl1, self.pl2]