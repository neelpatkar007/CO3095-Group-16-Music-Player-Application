import unittest
from unittest.mock import MagicMock
import io
import sys
from music_player.player_audio import change_volume

class TestConcolicDriven(unittest.TestCase):

    def setUp(self):
        self.held_output = io.StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_iteration_1_null_state(self):
        S1 = None
        S2 = "50"
        change_volume(S1, S2)
        self.assertEqual(self.held_output.getvalue(), "")

    def test_iteration_2_missing_structure(self):
        class EmptyState: pass

        S1 = EmptyState()
        S2 = "50"
        change_volume(S1, S2)
        self.assertEqual(self.held_output.getvalue(), "")

    def test_iteration_3_empty_input(self):
        class State:
            volume = 30
            audio_engine = None

        S1 = State()
        S2 = ""
        change_volume(S1, S2)
        self.assertIn("Current Volume: 30%", self.held_output.getvalue())

    def test_iteration_4_invalid_type_structure(self):
        class State:
            volume = 30
            audio_engine = None

        S1 = State()
        S2 = ["invalid"]
        change_volume(S1, S2)
        self.assertEqual(self.held_output.getvalue(), "")

    def test_iteration_5_conversion_error(self):
        class State:
            volume = 30
            audio_engine = None

        S1 = State()
        S2 = "NotANumber"
        change_volume(S1, S2)
        self.assertIn("Error: Volume must be a number", self.held_output.getvalue())

    def test_iteration_6_boundary_violation(self):
        class State:
            volume = 30
            audio_engine = None

        S1 = State()
        S2 = "-10"
        change_volume(S1, S2)
        self.assertIn("Error: Volume must be between 0 and 100", self.held_output.getvalue())

    def test_iteration_7_deep_state_mutation(self):
        mock_eng = MagicMock()

        class State:
            volume = 30
            audio_engine = mock_eng
            is_muted = True
            saved_volume = 30

        S1 = State()
        S2 = "75"
        change_volume(S1, S2)

        self.assertEqual(S1.is_muted, False)
        self.assertIn("Volume set to 75%", self.held_output.getvalue())

    def test_iteration_8_standard_success(self):
        mock_eng = MagicMock()

        class State:
            volume = 30
            audio_engine = mock_eng
            is_muted = False
            saved_volume = None

        S1 = State()
        S2 = "25"
        change_volume(S1, S2)
        mock_eng.set_muted.assert_not_called()
        mock_eng.set_volume.assert_called_with(25)
        self.assertIn("Volume set to 25%", self.held_output.getvalue())


if __name__ == '__main__':
    unittest.main()