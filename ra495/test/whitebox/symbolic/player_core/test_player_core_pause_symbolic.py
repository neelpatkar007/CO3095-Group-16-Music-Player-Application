import unittest
from unittest.mock import MagicMock
from music_player.player_core import pause

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.mock_state = MagicMock()
        self.mock_state.audio_engine = MagicMock()

    def test_pc_1_guard_hit(self):
        self.mock_state.is_playing = False
        self.mock_state.is_paused = False

        pause(self.mock_state)

        self.mock_state.audio_engine.pause.assert_not_called()
        self.assertFalse(self.mock_state.is_playing)

    def test_pc_2_action(self):
        self.mock_state.is_playing = True
        self.mock_state.is_paused = False

        pause(self.mock_state)

        self.mock_state.audio_engine.pause.assert_called_once()
        self.assertFalse(self.mock_state.is_playing, "S1 should be mutated to False")
        self.assertTrue(self.mock_state.is_paused, "S2 should be mutated to True")


if __name__ == '__main__':
    unittest.main()
