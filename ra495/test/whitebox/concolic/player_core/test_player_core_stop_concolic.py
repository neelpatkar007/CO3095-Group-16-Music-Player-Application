import unittest
from unittest.mock import MagicMock
import sys
from pathlib import Path


project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from music_player.player_core import stop

class PlayerState:
    def __init__(self, is_playing=True, is_paused=False):
        self.is_playing = is_playing
        self.is_paused = is_paused
        self.audio_engine = MagicMock()
        self.sleep_deadline = None
        self.position_seconds = 50.5



class TestConcolicExecution(unittest.TestCase):

    def test_iteration_1_concrete_idle(self):
        s1, s2 = False, False
        state = PlayerState(is_playing=s1, is_paused=s2)


        stop(state)


        state.audio_engine.stop.assert_not_called()
        self.assertEqual(state.position_seconds, 50.5)

    def test_iteration_2_derived_active(self):


        s1, s2 = True, False
        state = PlayerState(is_playing=s1, is_paused=s2)


        stop(state)

        state.audio_engine.stop.assert_called_once()
        self.assertEqual(state.position_seconds, 0.0)
        self.assertFalse(state.is_playing)
        self.assertFalse(state.is_paused)

if __name__ == '__main__':
    unittest.main()