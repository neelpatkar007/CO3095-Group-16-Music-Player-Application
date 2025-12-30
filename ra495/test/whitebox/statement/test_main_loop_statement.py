import unittest
from unittest.mock import MagicMock, patch
from music_player import main
from music_player.player_state import PlayerState


class TestMainLoops(unittest.TestCase):
    """
    White-Box Statement Coverage for main.py Loops.
    Testing Tool: Python unittest + unittest.mock
    Test Technique: Statement Testing (White-Box)
    """

    def setUp(self):
        self.state = PlayerState([], MagicMock())

