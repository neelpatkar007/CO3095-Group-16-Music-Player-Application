import unittest
from unittest.mock import MagicMock, Mock
from music_player.player_audio import toggle_mute

class TestSymbolicExecution(unittest.TestCase):

    def test_pc1_state_none(self):
        S1 = None
        toggle_mute(S1)

    def test_pc2_missing_attributes(self):
        S1 = Mock(spec=[])
        toggle_mute(S1)
        with self.assertRaises(AttributeError):
            _ = S1.is_muted

    def test_pc3_unmute_no_engine(self):
        S1 = Mock()
        S1.is_muted = True  # S4 = True
        S1.audio_engine = None  # S5 = False
        S1.saved_volume = 40
        S1.volume = 0
        toggle_mute(S1)

        self.assertFalse(S1.is_muted, "S4 should be negated (False)")
        self.assertEqual(S1.volume, 40, "Volume should be restored to saved_volume")

    def test_pc5_unmute_full_engine(self):
        S1 = Mock()
        S1.is_muted = True
        S1.saved_volume = 30
        S5 = Mock()
        S5.set_muted = Mock()
        S5.set_volume = Mock()
        S1.audio_engine = S5
        toggle_mute(S1)

        S5.set_muted.assert_called_with(False)
        S5.set_volume.assert_called_with(30)

    def test_pc6_mute_no_engine(self):
        S1 = Mock()
        S1.is_muted = False  # S4 = False
        S1.volume = 80
        S1.audio_engine = None  # S5 = False
        toggle_mute(S1)

        self.assertTrue(S1.is_muted)
        self.assertEqual(S1.saved_volume, 80)

    def test_pc8_mute_full_engine(self):
        S1 = Mock()
        S1.is_muted = False
        S1.volume = 75

        S5 = Mock()
        S5.set_muted = Mock()
        S5.set_volume = Mock()
        S1.audio_engine = S5
        toggle_mute(S1)

        self.assertEqual(S1.saved_volume, 75)
        S5.set_muted.assert_called_with(True)
        S5.set_volume.assert_called_with(0)


if __name__ == '__main__':
    unittest.main()