import unittest
from unittest.mock import MagicMock
import io
import sys
from music_player.player_audio import change_volume

class TestSymbolicExecution(unittest.TestCase):

    def setUp(self):
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_PC_1_state_none(self):
        S1 = None
        S2 = "50"
        change_volume(S1, S2)
        self.assertEqual(self.held_output.getvalue(), "")

    def test_PC_2_missing_attr(self):
        class IncompleteState:
            pass

        S1 = IncompleteState()
        S2 = "50"
        change_volume(S1, S2)
        self.assertEqual(self.held_output.getvalue(), "")

    def test_PC_3_empty_input(self):
        class ValidState:
            volume = 20
            audio_engine = MagicMock()

        S1 = ValidState()
        S2 = ""
        change_volume(S1, S2)
        self.assertIn("[audio] Current Volume: 20%", self.held_output.getvalue())

    def test_PC_4_invalid_type(self):
        class ValidState:
            volume = 20
            audio_engine = MagicMock()

        S1 = ValidState()
        S2 = [10]
        change_volume(S1, S2)
        self.assertEqual(self.held_output.getvalue(), "")

    def test_PC_5_conversion_fail(self):
        class ValidState:
            volume = 20
            audio_engine = MagicMock()

        S1 = ValidState()
        S2 = "five"
        change_volume(S1, S2)
        self.assertIn("Error: Volume must be a number", self.held_output.getvalue())

    def test_PC_6_range_fail(self):
        class ValidState:
            volume = 20
            audio_engine = MagicMock()

        S1 = ValidState()
        S2 = "150"
        change_volume(S1, S2)
        self.assertIn("Error: Volume must be between 0 and 100", self.held_output.getvalue())

    def test_PC_7_success_unmute(self):
        mock_engine = MagicMock()

        class FullState:
            volume = 10
            is_muted = True
            saved_volume = 10
            audio_engine = mock_engine

        S1 = FullState()
        S2 = "50"
        change_volume(S1, S2)

        self.assertEqual(S1.volume, 50)
        self.assertFalse(S1.is_muted)
        mock_engine.set_muted.assert_called_with(False)
        self.assertIn("Volume set to 50%", self.held_output.getvalue())

    def test_PC_8_success_std(self):
        mock_engine = MagicMock()

        class FullState:
            volume = 10
            is_muted = False
            saved_volume = None
            audio_engine = mock_engine

        S1 = FullState()
        S2 = "50"
        change_volume(S1, S2)

        self.assertEqual(S1.volume, 50)
        mock_engine.set_muted.assert_not_called()
        mock_engine.set_volume.assert_called_with(50)
        self.assertIn("Volume set to 50%", self.held_output.getvalue())


if __name__ == '__main__':
    unittest.main()