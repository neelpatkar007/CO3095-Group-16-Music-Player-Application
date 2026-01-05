import unittest
from unittest.mock import MagicMock
from music_player.player_audio import toggle_mute

class TestConcolicExecution(unittest.TestCase):

    def test_iteration_1_flip_S1(self):
        S1 = None
        toggle_mute(S1)

    def test_iteration_2_flip_S2_S3(self):
        class EmptyState:
            pass

        S1 = EmptyState()
        toggle_mute(S1)

        self.assertFalse(hasattr(S1, 'is_muted'))

    def test_iteration_3_flip_S4_Branch_A(self):
        S1 = MagicMock()
        S1.is_muted = True
        S1.audio_engine = MagicMock()  # S5 True

        toggle_mute(S1)

        self.assertFalse(S1.is_muted)
        S1.audio_engine.set_muted.assert_called_with(False)

    def test_iteration_4_flip_S4_Branch_B(self):
        S1 = MagicMock()
        S1.is_muted = False
        S1.audio_engine = MagicMock()

        toggle_mute(S1)

        self.assertTrue(S1.is_muted)
        S1.audio_engine.set_muted.assert_called_with(True)


if __name__ == '__main__':
    unittest.main()