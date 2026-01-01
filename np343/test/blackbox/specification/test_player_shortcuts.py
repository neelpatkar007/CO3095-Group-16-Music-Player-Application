import unittest
from unittest.mock import MagicMock, patch
from music_player import player_shortcuts
from music_player.player_state import PlayerState


class TestPlayerShortcutsSpec(unittest.TestCase):
    """
    Black-Box Specification Testing for player_shortcuts.py.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Black-Box Specification Testing
    """

    def setUp(self):
        self.state = MagicMock(spec=PlayerState)
        self.state.tracks = [MagicMock()]  # Ensure tracks exist by default
        self.state.is_playing = False
        self.state.volume = 50