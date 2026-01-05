import unittest
from unittest.mock import MagicMock
import sys
from pathlib import Path

from music_player.player_core import stop

class PlayerState:
    def __init__(self, is_playing: bool = True, is_paused: bool = False):
        self.is_playing = is_playing
        self.is_paused = is_paused
        self.audio_engine = MagicMock()
        self.sleep_deadline = None
        self.position_seconds = 100.0



class TestSymbolicExecution(unittest.TestCase):

    def test_pc_1_idle_state(self):

        s1 = False
        s2 = False
        state = PlayerState(is_playing=s1, is_paused=s2)

        stop(state)

        state.audio_engine.stop.assert_not_called()
        self.assertEqual(state.position_seconds, 100.0)

    def test_pc_2_active_state(self):
        s1 = True
        s2 = False
        state = PlayerState(is_playing=s1, is_paused=s2)

        stop(state)

        state.audio_engine.stop.assert_called_once()
        self.assertFalse(state.is_playing)
        self.assertFalse(state.is_paused)
        self.assertEqual(state.position_seconds, 0.0)


if __name__ == '__main__':
    unittest.main()